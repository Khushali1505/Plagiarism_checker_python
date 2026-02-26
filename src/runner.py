#src/runner.py
import argparse
import os
import webbrowser
import itertools
from src.checker import compare_files

def compare_single(file1, file2, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    html_file = os.path.join(output_dir, f"{os.path.basename(file1)}_vs_{os.path.basename(file2)}.html")
    result = compare_files(file1, file2, include_legend=True)
    html_content = f"<html><body>{result['html_content']}</body></html>"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"{file1} ↔ {file2} comparison saved at {html_file}")
    webbrowser.open("file://" + os.path.abspath(html_file))

def compare_batch(folder, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    py_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".py")]
    if len(py_files) < 2:
        print("⚠️ Not enough files to compare")
        return

    batch_html = """
    <html>
    <head>
    <style>
        .collapsible {
            background-color: #eee;
            cursor: pointer;
            padding: 6px;
            width: 100%;
            border: none;
            text-align: left;
            outline: none;
            font-size: 14px;
            font-family: monospace;
            margin-bottom: 2px;
        }
        .active, .collapsible:hover {
            background-color: #ccc;
        }
        .content {
            padding: 0 10px;
            display: none;
            overflow: hidden;
            border-left: 2px solid #ccc;
            margin-bottom: 8px;
        }
        table { border-collapse: collapse; width: 100%; font-family: monospace; }
        td { vertical-align: top; padding:2px 4px; white-space: pre; }
        .legend-table td { padding:1px 4px; font-size:12px; }
    </style>
    </head>
    <body>
    <h2>Batch Code Comparison (Collapsible)</h2>
    <!-- Compact Legend -->
    <table class="legend-table" style="border:1px solid #ccc; margin-bottom:5px;">
        <tr>
            <td style="background:#ffcccc; width:15px;"></td><td>Removed/Changed in left file</td>
        </tr>
        <tr>
            <td style="background:#ffff99;"></td><td>Added/Changed in right file</td>
        </tr>
        <tr>
            <td style="background:#d4fcbc;"></td><td>Equal</td>
        </tr>
    </table>
    """

    for f1, f2 in itertools.combinations(py_files, 2):
        result = compare_files(f1, f2, include_legend=False)
        batch_html += f"""
        <button class="collapsible">{os.path.basename(f1)} ↔ {os.path.basename(f2)}</button>
        <div class="content">{result['html_content']}</div>
        """

    batch_html += """
    <script>
        var coll = document.getElementsByClassName("collapsible");
        for (var i = 0; i < coll.length; i++) {
            coll[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.display === "block") {
                    content.style.display = "none";
                } else {
                    content.style.display = "block";
                }
            });
        }
    </script>
    </body>
    </html>
    """

    batch_file = os.path.join(output_dir, "batch_comparison.html")
    with open(batch_file, "w", encoding="utf-8") as f:
        f.write(batch_html)

    print(f"\n✅ Batch comparison saved at {batch_file}")
    webbrowser.open("file://" + os.path.abspath(batch_file))

def main():
    parser = argparse.ArgumentParser(description="Python Code Comparison Tool")
    parser.add_argument("--file1", help="First file for single comparison")
    parser.add_argument("--file2", help="Second file for single comparison")
    parser.add_argument("--batch", help="Folder path for batch comparison")
    parser.add_argument("--out", help="Output folder (optional)")
    args = parser.parse_args()

    output_dir = args.out if args.out else "outputs"

    if args.file1 and args.file2:
        compare_single(args.file1, args.file2, output_dir)
    elif args.batch:
        compare_batch(args.batch, output_dir)
    else:
        print("❌ Provide either single files (--file1 & --file2) or batch (--batch)")

if __name__=="__main__":
    main()
