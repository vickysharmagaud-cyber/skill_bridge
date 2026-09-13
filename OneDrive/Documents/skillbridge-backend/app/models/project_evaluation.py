from sqlalchemy import Column, Integer, Float, Text, ForeignKey

from app.database.database import Base


class ProjectEvaluation(Base):
    __tablename__ = "project_evaluations"

    id = Column(Integer, primary_key=True, index=True)

    submission_id = Column(
        Integer,
        ForeignKey("project_submissions.id"),
        nullable=False
    )

    implementation_score = Column(Float, default=0)
    project_understanding_score = Column(Float, default=0)

    feedback = Column(Text, nullable=True)