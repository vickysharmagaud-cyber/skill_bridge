from pydantic import BaseModel


class TopicAssessmentAnswerCreate(BaseModel):
    question_id: int
    selected_answer: str