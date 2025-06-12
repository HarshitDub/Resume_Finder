# auth.py

import bcrypt
import pandas as pd
from pathlib import Path

AUTH_FILE = Path("data/users.csv")
AUTH_FILE.parent.mkdir(exist_ok=True)

def init_auth_storage():
    if not AUTH_FILE.exists():
        df = pd.DataFrame(columns=["email", "hashed_password"])
        df.to_csv(AUTH_FILE, index=False)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def signup(email: str, password: str) -> bool:
    df = pd.read_csv(AUTH_FILE)
    if email in df["email"].values:
        return False  # user already exists
    hashed = hash_password(password)
    new_row = pd.DataFrame([{"email": email, "hashed_password": hashed}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(AUTH_FILE, index=False)
    return True

def login(email: str, password: str) -> bool:
    df = pd.read_csv(AUTH_FILE)
    user = df[df["email"] == email]
    if user.empty:
        return False
    stored_hash = user.iloc[0]["hashed_password"]
    return verify_password(password, stored_hash)
