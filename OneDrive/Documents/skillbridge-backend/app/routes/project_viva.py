from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.project_viva import ProjectViva
from app.models.project_submission import ProjectSubmission
from app.schemas.project_viva import (
    ProjectVivaCreate,
    ProjectVivaAnswer,
    ProjectVivaEvaluation
)


router = APIRouter(
    prefix="/project-vivas",
    tags=["Project Viva"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{submission_id}")
def create_viva_question(
    submission_id: int,
    data: ProjectVivaCreate,
    db: Session = Depends(get_db)
):
    submission = db.query(ProjectSubmission).filter(
        ProjectSubmission.id == submission_id
    ).first()

    if not submission:
        return {
            "message": "Project submission not found"
        }

    viva = ProjectViva(
        submission_id=submission_id,
        question=data.question
    )

    db.add(viva)
    db.commit()
    db.refresh(viva)

    return {
        "message": "Viva question created",
        "viva_id": viva.id,
        "submission_id": viva.submission_id,
        "question": viva.question
    }

@router.put("/{viva_id}/answer")
def submit_viva_answer(
    viva_id: int,
    data: ProjectVivaAnswer,
    db: Session = Depends(get_db)
):
    viva = db.query(ProjectViva).filter(
        ProjectViva.id == viva_id
    ).first()

    if not viva:
        return {
            "message": "Viva question not found"
        }

    viva.answer = data.answer

    db.commit()
    db.refresh(viva)

    return {
        "message": "Viva answer saved",
        "viva_id": viva.id,
        "question": viva.question,
        "answer": viva.answer
    }

@router.put("/{viva_id}/evaluate")
def evaluate_viva(
    viva_id: int,
    data: ProjectVivaEvaluation,
    db: Session = Depends(get_db)
):
    viva = db.query(ProjectViva).filter(
        ProjectViva.id == viva_id
    ).first()

    if not viva:
        return {
            "message": "Viva question not found"
        }

    if viva.answer is None:
        return {
            "message": "Viva answer not submitted yet"
        }

    if data.score < 0 or data.score > 10:
        return {
            "message": "Score must be between 0 and 10"
        }

    viva.score = data.score

    db.commit()
    db.refresh(viva)

    return {
        "message": "Viva evaluated",
        "viva_id": viva.id,
        "question": viva.question,
        "answer": viva.answer,
        "score": viva.score
    }