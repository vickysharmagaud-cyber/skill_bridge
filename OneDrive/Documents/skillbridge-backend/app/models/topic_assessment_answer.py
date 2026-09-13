from sqlalchemy import Column, Integer, String, ForeignKey

from app.database.database import Base


class TopicAssessmentAnswer(Base):
    __tablename__ = "topic_assessment_answers"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(
        Integer,
        ForeignKey("topic_assessments.id"),
        nullable=False
    )
    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )
    selected_answer = Column(String(1), nullable=False)