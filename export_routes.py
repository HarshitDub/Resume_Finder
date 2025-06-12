# routes/export_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from utils import export_to_excel, export_to_csv
import pandas as pd

router = APIRouter()

class ExportRequest(BaseModel):
    data: List[Dict]
    filename: str = "profiles"

@router.post("/excel")
def export_excel(req: ExportRequest):
    try:
        df = pd.DataFrame(req.data)
        filepath = export_to_excel(df, filename=f"{req.filename}.xlsx")
        return {"message": "✅ Excel file created", "file_path": str(filepath)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/csv")
def export_csv(req: ExportRequest):
    try:
        df = pd.DataFrame(req.data)
        filepath = export_to_csv(df, filename=f"{req.filename}.csv")
        return {"message": "✅ CSV file created", "file_path": str(filepath)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
