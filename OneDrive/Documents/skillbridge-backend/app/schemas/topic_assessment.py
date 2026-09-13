from pydantic import BaseModel
from app.schemas.question import QuestionResponse


class TopicQuestionsResponse(BaseModel):
    assessment_id: int
    skill_id: int
    questions: list[QuestionResponse]