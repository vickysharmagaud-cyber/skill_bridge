from pydantic import BaseModel


class ProjectEvaluationCreate(BaseModel):
    implementation_score: float
    project_understanding_score: float
    feedback: str | None = None