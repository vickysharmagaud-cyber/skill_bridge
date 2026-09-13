from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.project import Project
from app.models.skill import Skill
from app.schemas.project import ProjectCreate


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(
        Skill.id == data.skill_id
    ).first()

    if not skill:
        return {
            "message": "Skill not found"
        }

    project = Project(
        title=data.title,
        description=data.description,
        skill_id=data.skill_id,
        difficulty=data.difficulty
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "message": "Project created",
        "project_id": project.id,
        "title": project.title,
        "skill_id": project.skill_id,
        "difficulty": project.difficulty
    }