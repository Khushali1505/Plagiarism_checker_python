# src/core.py
import io
import tokenize
from difflib import SequenceMatcher
import ast
from pathlib import Path
import difflib
import webbrowser
import os

def remove_comments_and_docstrings(source):
    """Remove comments and docstrings using tokenize; fallback to original if fails."""
    try:
        io_obj = io.StringIO(source)
        out_tokens = []
        prev_toktype = tokenize.INDENT
        first_line = True
        for tok in tokenize.generate_tokens(io_obj.readline):
            tok_type = tok.type
            tok_string = tok.string

            if tok_type == tokenize.COMMENT:
                continue

            if tok_type == tokenize.STRING:
                if prev_toktype == tokenize.INDENT or prev_toktype == tokenize.NEWLINE or first_line:
                    prev_toktype = tok_type
                    first_line = False
                    continue

            out_tokens.append(tok_string)
            prev_toktype = tok_type
            first_line = False
        return "".join(out_tokens)
    except Exception:
        return source

def normalize_whitespace(source):
    return " ".join(source.split())

def preprocess_code(source):
    s = remove_comments_and_docstrings(source)
    s = normalize_whitespace(s)
    return s

def text_similarity(code1, code2):
    return SequenceMatcher(None, code1, code2).ratio()

class NameNormalizer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.name_map = {}
        self.counter = 0
    def _map(self, original):
        if original in self.name_map:
            return self.name_map[original]
        self.counter += 1
        new = f'id_{self.counter}'
        self.name_map[original] = new
        return new
    def visit_Name(self, node):
        try:
            new_id = self._map(node.id)
            return ast.copy_location(ast.Name(id=new_id, ctx=node.ctx), node)
        except Exception:
            return node
    def visit_arg(self, node):
        try:
            node.arg = self._map(node.arg)
            return node
        except Exception:
            return node
    def visit_FunctionDef(self, node):
        try:
            node.name = self._map(node.name)
            self.generic_visit(node)
            return node
        except Exception:
            return node
    def visit_ClassDef(self, node):
        try:
            node.name = self._map(node.name)
            self.generic_visit(node)
            return node
        except Exception:
            return node

def ast_structure_string(source):
    try:
        tree = ast.parse(source)
    except Exception:
        return ""
    normalizer = NameNormalizer()
    tree = normalizer.visit(tree)
    return ast.dump(tree, annotate_fields=False, include_attributes=False)

def ast_similarity(code1, code2):
    s1 = ast_structure_string(code1)
    s2 = ast_structure_string(code2)
    if not s1 or not s2:
        return 0.0
    return SequenceMatcher(None, s1, s2).ratio()

def combined_score(text_score, ast_score, w_text=0.45, w_ast=0.55):
    return w_text * text_score + w_ast * ast_score

def generate_html_diff(path_a, path_b, out_html):
    a = Path(path_a).read_text(encoding="utf-8", errors="ignore").splitlines()
    b = Path(path_b).read_text(encoding="utf-8", errors="ignore").splitlines()
    diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=80)
    html = diff.make_file(a, b, fromdesc=path_a, todesc=path_b)
    os.makedirs(os.path.dirname(out_html), exist_ok=True)
    Path(out_html).write_text(html, encoding="utf-8")
    try:
        webbrowser.open(Path(out_html).absolute().as_uri())
    except Exception:
        pass

def compare_files(file_a, file_b, html_report_path="outputs/compare.html"):
    a_src = Path(file_a).read_text(encoding="utf-8", errors="ignore")
    b_src = Path(file_b).read_text(encoding="utf-8", errors="ignore")

    a_proc = preprocess_code(a_src)
    b_proc = preprocess_code(b_src)

    t_score = text_similarity(a_proc, b_proc)
    ast_score = ast_similarity(a_proc, b_proc)
    final = combined_score(t_score, ast_score)

    if html_report_path:
        generate_html_diff(file_a, file_b, html_report_path)

    return {
        "file_a": str(file_a),
        "file_b": str(file_b),
        "text_score": t_score,
        "ast_score": ast_score,
        "combined_score": final,
        "html_report": html_report_path
    }
