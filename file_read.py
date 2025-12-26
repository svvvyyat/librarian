import os
import pandas as pd
from pypdf import PdfReader
import docx

def get_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.pdf':
            return read_pdf(file_path)
        elif ext == '.docx':
            return read_docx(file_path)
        #elif ext in ['xls', 'xlsx', 'csv']:
            #return read_xls(file_path)
        elif ext == '.txt':
            return read_txt(file_path)
        else:
            return None
    except Exception as e:
        print(f"Помилка читання {file_path}: {e}")
        return None
def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
def read_docx(file_path):
    return None
def read_pdf(file_path):
    return None