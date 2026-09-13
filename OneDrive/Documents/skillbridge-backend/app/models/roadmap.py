from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    status = Column(String(50), default="Not Started")
    priority = Column(Integer, default=1)