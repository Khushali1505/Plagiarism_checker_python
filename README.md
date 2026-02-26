# Python Plagiarism Checker

A Python-based code similarity analysis tool that compares multiple source files
and identifies similarity using tokenization and sequence matching techniques.

## Features
- Removes comments and docstrings for fair comparison
- Compares multiple Python files
- Generates similarity scores between submissions
- Supports batch processing of files
- Modular and extensible design

## Tech Stack
- Python
- difflib (SequenceMatcher)
- tokenize, ast
- File handling and preprocessing

## Use Case
Designed to analyze similarity between student code submissions and assist in
basic plagiarism detection and code comparison workflows.

## Project Structure
- src/ : core logic
- testcode/ : sample files for testing
- outputs/ : generated results

## Future Scope
- Language-agnostic comparison
- Improved scoring logic
- Integration with web or dashboard interface
