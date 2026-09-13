from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.project_submission import ProjectSubmission
from app.models.user import User
from app.models.project import Project
from app.schemas.project_submission import ProjectSubmissionCreate


router = APIRouter(
    prefix="/project-submissions",
    tags=["Project Submissions"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{user_id}")
def submit_project(
    user_id: int,
    data: ProjectSubmissionCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {
            "message": "User not found"
        }

    project = db.query(Project).filter(
        Project.id == data.project_id
    ).first()

    if not project:
        return {
            "message": "Project not found"
        }

    submission = ProjectSubmission(
        user_id=user_id,
        project_id=data.project_id,
        github_url=data.github_url,
        submission_text=data.submission_text,
        status="Submitted"
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return {
        "message": "Project submitted",
        "submission_id": submission.id,
        "user_id": submission.user_id,
        "project_id": submission.project_id,
        "github_url": submission.github_url,
        "status": submission.status
    }