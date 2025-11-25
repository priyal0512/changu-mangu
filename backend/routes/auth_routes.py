# backend/routes/auth_routes.py

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from database.mongodb_config import db

# ✅ define router (required by FastAPI)
router = APIRouter()

class AuthRequest(BaseModel):
    name: str | None = None
    email: EmailStr
    password: str

@router.post("/signup")
async def signup(user: AuthRequest):
    """
    Register a new user and store credentials in MongoDB.
    """
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        return {"error": "User already exists"}

    doc = user.dict()
    await db["users"].insert_one(doc)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: AuthRequest):
    """
    Authenticate an existing user.
    """
    record = await db["users"].find_one(
        {"email": user.email, "password": user.password}
    )
    if record:
        return {"message": "Login successful"}
    return {"error": "Invalid credentials"}
