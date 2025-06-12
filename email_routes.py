# routes/email_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from emailer import send_email_gmail, send_email_ses
from pathlib import Path

router = APIRouter()

class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    message: str
    method: str  # 'gmail' or 'ses'
    file_path: str  # Path to local file to send

@router.post("/")
def send_email(data: EmailRequest):
    path = Path(data.file_path)

    if not path.exists():
        raise HTTPException(status_code=400, detail="Attachment file does not exist")

    try:
        if data.method.lower() == "gmail":
            success = send_email_gmail(data.to_email, data.subject, data.message, path)
        elif data.method.lower() == "ses":
            success = send_email_ses(data.to_email, data.subject, data.message, path)
        else:
            raise HTTPException(status_code=400, detail="Invalid method: use 'gmail' or 'ses'")

        if success:
            return {"message": "✅ Email sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Email sending failed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
