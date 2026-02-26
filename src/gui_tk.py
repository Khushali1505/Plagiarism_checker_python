# src/gui_tk.py
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import webbrowser
from src.runner import compare_single, compare_batch

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

def run_single():
    """Run single file comparison."""
    file1 = filedialog.askopenfilename(title="Select first Python file", filetypes=[("Python Files", "*.py")])
    file2 = filedialog.askopenfilename(title="Select second Python file", filetypes=[("Python Files", "*.py")])
    if file1 and file2:
        compare_single(file1, file2, output_dir)
        messagebox.showinfo("Done", f"Comparison done! HTML report saved in {output_dir}")
        html_file = os.path.join(output_dir, f"{os.path.basename(file1)}_vs_{os.path.basename(file2)}.html")
        if os.path.exists(html_file):
            webbrowser.open("file://" + os.path.abspath(html_file))

def run_batch():
    """Run batch comparison on a folder."""
    folder = filedialog.askdirectory(title="Select folder with Python files")
    if folder:
        compare_batch(folder, output_dir)
        messagebox.showinfo("Done", f"Batch comparison done! Reports saved in {output_dir}")

        html_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".html")]
        for html_file in html_files:
            webbrowser.open("file://" + os.path.abspath(html_file))

root = tk.Tk()
root.title("Python Plagiarism Checker")
root.geometry("400x200") 

tk.Label(root, text="Python Plagiarism Checker", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(root, text="Single File Comparison", command=run_single, width=30, height=2).pack(pady=10)
tk.Button(root, text="Batch Folder Comparison", command=run_batch, width=30, height=2).pack(pady=10)

root.mainloop()
