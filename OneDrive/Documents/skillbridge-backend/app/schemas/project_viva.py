from pydantic import BaseModel


class ProjectVivaCreate(BaseModel):
    question: str


class ProjectVivaAnswer(BaseModel):
    answer: str


class ProjectVivaEvaluation(BaseModel):
    score: int