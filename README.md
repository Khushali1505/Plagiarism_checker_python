# Python Plagiarism Checker

A simple tool to detect similarities between Python `.py` files. It helps teachers, students, or developers check if code is copied or too similar. The tool works for **single file comparison** as well as **multiple files in batch**, and shows the results in an easy-to-read **web interface**.

---

## What It Does

- Compares **two Python files** or multiple files at once.  
- Shows **Text similarity** (exact lines and words) and **AST similarity** (structure of the code).  
- Gives a **combined score** showing how similar the files are.  
- Highlights **differences and similarities** in color in the results.  
- Works entirely in your **web browser** using **Streamlit**.  

---

## Who Can Use It

- **Teachers:** Check student submissions for copied code.  
- **Students:** Make sure your code is original.  
- **Developers:** Compare code versions or detect accidental copying.  

---

## How It Works

1. Upload Python files (`.py`) or a ZIP file containing multiple Python files.  
2. The tool compares files **word by word** and **structure by structure**.  
3. Results are shown in the browser in a **color-coded format**:  
   - **Red:** Differences  
   - **Green:** Similarities  
   - **Blue:** Partial matches  
4. Batch comparisons show all results in **collapsible sections** for easy navigation.  

---

## Future Scope
- Language-agnostic comparison
- Improved scoring logic
- Integration with web or dashboard interface

## How to Use

1. Make sure you have Python 3.9+ installed.  
2. Install Streamlit:

```bash
pip install streamlit

Run the web interface:

python -m src.web_streamlit

Upload your .py files or a ZIP file of multiple Python files.

View the comparison results directly in your browser.

