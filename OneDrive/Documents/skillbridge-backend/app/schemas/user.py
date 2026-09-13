from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    education: str | None = None
    branch: str | None = None
    year: int | None = None
    preferred_language: str = "English"
    career_goal: str | None = None