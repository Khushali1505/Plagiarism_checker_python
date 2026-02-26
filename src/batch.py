# src/batch.py

from pathlib import Path
from itertools import combinations
import csv
import os
from src.checker import compare_files  

def batch_compare(folder, out_csv="outputs/report.csv", html_dir="outputs/html_reports"):
    p = Path(folder)
    py_files = sorted([f for f in p.glob("*.py")])
    if not py_files:
        print("⚠️ No Python files found in folder:", folder)
        return

    os.makedirs(html_dir, exist_ok=True)

    rows = []
    for f1, f2 in combinations(py_files, 2):
        html_path = Path(html_dir) / f"{f1.stem}_vs_{f2.stem}.html"
        print(f"🔍 Comparing {f1.name} ↔ {f2.name} ...")
        compare_files(str(f1), str(f2))
        rows.append({
            "file_a": f1.name,
            "file_b": f2.name,
        })

    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file_a", "file_b"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Batch comparison complete! Results saved in: {out_csv}")
    print(f"Check the HTML reports in: {html_dir}")
