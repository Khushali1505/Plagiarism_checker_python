#src/checker.py
import difflib
import ast
import os
from html import escape
import re

def tokenize_line(line):
    """Split a line into meaningful Python tokens (words, numbers, punctuations) and preserve spaces."""
    tokens = re.findall(r'\s+|\w+|[^\s\w]', line)
    return tokens

def ast_similarity(file1, file2):
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        tree1 = ast.dump(ast.parse(f1.read()))
        tree2 = ast.dump(ast.parse(f2.read()))
    return round(difflib.SequenceMatcher(None, tree1, tree2).ratio()*100, 2)

def text_similarity(file1, file2):
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        text1 = f1.read()
        text2 = f2.read()
    return round(difflib.SequenceMatcher(None, text1, text2).ratio()*100, 2)

def highlight_tokens(tokens1, tokens2):
    """Highlight only different tokens."""
    matcher = difflib.SequenceMatcher(None, tokens1, tokens2)
    out1, out2 = "", ""
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        seg1 = ''.join(tokens1[i1:i2])
        seg2 = ''.join(tokens2[j1:j2])
        if tag == 'equal':
            out1 += f"<span style='background:#d4fcbc'>{escape(seg1)}</span>"
            out2 += f"<span style='background:#d4fcbc'>{escape(seg2)}</span>"
        elif tag == 'replace':
            out1 += f"<span style='background:#ffcccc'>{escape(seg1)}</span>"
            out2 += f"<span style='background:#ffff99'>{escape(seg2)}</span>"
        elif tag == 'delete':
            out1 += f"<span style='background:#ffcccc'>{escape(seg1)}</span>"
        elif tag == 'insert':
            out2 += f"<span style='background:#ffff99'>{escape(seg2)}</span>"
    return out1, out2

def generate_side_by_side_html(file1, file2, text_score, ast_score, combined_score, include_legend=True):
    """Return HTML content for a single comparison with optional legend."""
    with open(file1, "r", encoding="utf-8") as f:
        lines1 = f.readlines()
    with open(file2, "r", encoding="utf-8") as f:
        lines2 = f.readlines()

    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    html_rows = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        max_lines = max(i2 - i1, j2 - j1)
        for n in range(max_lines):
            line1 = lines1[i1+n].rstrip() if i1+n < i2 else ""
            line2 = lines2[j1+n].rstrip() if j1+n < j2 else ""
            tokens1 = tokenize_line(line1)
            tokens2 = tokenize_line(line2)
            h1, h2 = highlight_tokens(tokens1, tokens2)
            html_rows.append(f"<tr><td>{h1}</td><td>{h2}</td></tr>")

    legend_html = ""
    if include_legend:
        legend_html = """
        <table style="margin-bottom:10px; font-family:Arial; font-size:12px; border-collapse:collapse;">
            <tr>
                <td style="background:#ffcccc; padding:2px 6px;"></td>
                <td style="padding:2px 6px;">Removed/Changed in left file</td>
                <td style="background:#ffff99; padding:2px 6px;"></td>
                <td style="padding:2px 6px;">Added/Changed in right file</td>
                <td style="background:#d4fcbc; padding:2px 6px;"></td>
                <td style="padding:2px 6px;">Equal</td>
            </tr>
        </table>
        """

    html_content = f"""
    {legend_html}
    <h3>{os.path.basename(file1)} ↔ {os.path.basename(file2)}</h3>
    <table style='border-collapse:collapse; width:100%; font-family:monospace;'>
        {''.join(html_rows)}
    </table>
    <p><strong>Text Score:</strong> {text_score} | <strong>AST Score:</strong> {ast_score} | <strong>Combined:</strong> {combined_score}</p>
    <hr>
    """
    return html_content

def compare_files(file1, file2, include_legend=True):
    t_score = text_similarity(file1, file2)
    a_score = ast_similarity(file1, file2)
    combined = round((t_score*0.5 + a_score*0.5), 2)
    html_content = generate_side_by_side_html(file1, file2, t_score, a_score, combined, include_legend)
    return {"file1": file1, "file2": file2, "text_score": t_score, "ast_score": a_score, "combined": combined, "html_content": html_content}
