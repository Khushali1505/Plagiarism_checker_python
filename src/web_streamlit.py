# src/web_streamlit.py
import streamlit as st
import os
import tempfile
from src.runner import compare_single, compare_batch
import streamlit.components.v1 as components
from zipfile import ZipFile

st.set_page_config(page_title="Python Plagiarism Checker", layout="wide")
st.title("Python Plagiarism Checker (Streamlit Demo)")

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

st.header("Single File Comparison")
f1 = st.file_uploader("Upload first .py file", type="py", key="f1")
f2 = st.file_uploader("Upload second .py file", type="py", key="f2")

if f1 and f2:
    tmp1 = os.path.join(tempfile.gettempdir(), f1.name)
    tmp2 = os.path.join(tempfile.gettempdir(), f2.name)
    with open(tmp1, "wb") as file: file.write(f1.getbuffer())
    with open(tmp2, "wb") as file: file.write(f2.getbuffer())

    html_file = os.path.join(output_dir, f"{f1.name}_vs_{f2.name}.html")
    compare_single(tmp1, tmp2, output_dir=output_dir)

    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.subheader("Comparison Result")
    components.html(html_content, height=600, scrolling=True)

st.header("Batch Comparison (Upload ZIP)")
zip_file = st.file_uploader("Upload ZIP folder containing multiple .py files", type="zip", key="batch")

if zip_file:
    tmp_zip = os.path.join(tempfile.gettempdir(), zip_file.name)
    with open(tmp_zip, "wb") as f: f.write(zip_file.getbuffer())

    batch_folder = os.path.join(tempfile.gettempdir(), "batch_files")
    os.makedirs(batch_folder, exist_ok=True)
    with ZipFile(tmp_zip, 'r') as zip_ref:
        zip_ref.extractall(batch_folder)

    compare_batch(batch_folder, output_dir=output_dir)

    st.subheader("Batch Comparison Results")
    html_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".html")]
    for html_file in html_files:
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        filename = os.path.basename(html_file).replace("_", " vs ")
        with st.expander(filename):
            components.html(html_content, height=400, scrolling=True)
