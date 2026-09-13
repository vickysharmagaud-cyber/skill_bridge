from sqlalchemy import Column, Integer, Text, ForeignKey

from app.database.database import Base


class ProjectViva(Base):
    __tablename__ = "project_vivas"

    id = Column(Integer, primary_key=True, index=True)

    submission_id = Column(
        Integer,
        ForeignKey("project_submissions.id"),
        nullable=False
    )

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    score = Column(Integer, nullable=True)