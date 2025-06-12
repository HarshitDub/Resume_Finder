# routes/scrape_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from scraper import scrape_linkedin_profiles
import pandas as pd

router = APIRouter()

# Define request body structure
class ScrapeRequest(BaseModel):
    role: str
    experience: str
    company: str = ""
    max_results: int = 10

@router.post("/")
def fetch_profiles(data: ScrapeRequest):
    try:
        query = f"{data.role} with {data.experience} experience"
        if data.company:
            query += f" at {data.company}"

        df: pd.DataFrame = scrape_linkedin_profiles(query, data.max_results)
        records = df.to_dict(orient="records")
        return {"results": records, "count": len(records)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
