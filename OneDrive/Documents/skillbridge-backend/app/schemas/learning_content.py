from pydantic import BaseModel


class LearningContentCreate(BaseModel):
    skill_id: int
    title: str
    content: str
    order: int = 1