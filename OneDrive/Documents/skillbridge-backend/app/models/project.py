from sqlalchemy import Column, Integer, String, Text, ForeignKey

from app.database.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    difficulty = Column(String(50), default="Beginner")