from pydantic import BaseModel, ConfigDict


class QuestionResponse(BaseModel):
    id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    skill_id: int

    model_config = ConfigDict(from_attributes=True)