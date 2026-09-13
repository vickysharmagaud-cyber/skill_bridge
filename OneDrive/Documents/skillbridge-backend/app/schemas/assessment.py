from pydantic import BaseModel


class AnswerCreate(BaseModel):
    question_id: int
    selected_answer: str