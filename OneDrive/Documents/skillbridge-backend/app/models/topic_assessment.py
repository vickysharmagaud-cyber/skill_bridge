from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from datetime import datetime

from app.database.database import Base


class TopicAssessment(Base):
    __tablename__ = "topic_assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    score = Column(Float, default=0)
    completed_at = Column(DateTime, default=datetime.utcnow)