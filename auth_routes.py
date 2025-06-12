# routes/auth_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from auth import login, signup, init_auth_storage

router = APIRouter()
init_auth_storage()

# Request schema
class AuthRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
def signup_user(data: AuthRequest):
    if signup(data.email, data.password):
        return {"message": "✅ Signup successful"}
    raise HTTPException(status_code=400, detail="User already exists")

@router.post("/login")
def login_user(data: AuthRequest):
    if login(data.email, data.password):
        return {"message": "✅ Login successful"}
    raise HTTPException(status_code=401, detail="Invalid email or password")
