from sqlalchemy import Column, Integer, String, Text, ForeignKey

from app.database.database import Base


class ProjectSubmission(Base):
    __tablename__ = "project_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    github_url = Column(String(500), nullable=True)
    submission_text = Column(Text, nullable=True)

    status = Column(String(50), default="Submitted")
    score = Column(Integer, nullable=True)