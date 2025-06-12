# utils.py

import pandas as pd
import base64
from io import BytesIO, StringIO
from pathlib import Path

def export_to_excel(df, filename="exported_data.xlsx"):
    filepath = Path("data") / filename
    filepath.parent.mkdir(exist_ok=True)
    df.to_excel(filepath, index=False, engine="openpyxl")
    return filepath

def export_to_csv(df, filename="exported_data.csv"):
    filepath = Path("data") / filename
    filepath.parent.mkdir(exist_ok=True)
    df.to_csv(filepath, index=False)
    return filepath

def get_download_link_excel(df, filename="data.xlsx", label="📥 Download Excel"):
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{label}</a>'
    return href

def get_download_link_csv(df, filename="data.csv", label="📥 Download CSV"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{label}</a>'
    return href
