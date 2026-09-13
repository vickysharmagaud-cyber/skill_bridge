from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    description: str
    skill_id: int
    difficulty: str = "Beginner"