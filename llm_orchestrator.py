# llm_orchestrator.py

from scraper import scrape_linkedin_profiles
from utils import export_to_excel
from emailer import send_email_gmail
import pandas as pd
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_prompt(prompt: str, user_email: str):
    # Step 1: Use GPT to interpret the task
    system_prompt = (
        "You are an assistant that receives user prompts about finding candidates "
        "and automating outreach. Extract the job role, experience, company (optional), "
        "and compose a professional email."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message["content"]

    # Assume the LLM returns structured JSON-like text
    import re, json
    json_block = re.search(r"\{.*\}", result, re.DOTALL)
    if not json_block:
        raise ValueError("LLM did not return structured data.")

    data = json.loads(json_block.group())

    # Step 2: Scrape data
    query = f"{data['role']} with {data['experience']} experience"
    if data.get("company"):
        query += f" at {data['company']}"

    df: pd.DataFrame = scrape_linkedin_profiles(query, max_results=10)
    file_path = export_to_excel(df, filename="llm_profiles.xlsx")

    # Step 3: Compose and send email
    subject = data.get("subject", f"Candidate Profiles for {data['role']}")
    body = data.get("email_body", "Please find attached the filtered candidate list.")
    success = send_email_gmail(user_email, subject, body, file_path)

    return {
        "message": "✅ Process completed",
        "email_sent": success,
        "file_path": str(file_path),
        "extracted": data
    }