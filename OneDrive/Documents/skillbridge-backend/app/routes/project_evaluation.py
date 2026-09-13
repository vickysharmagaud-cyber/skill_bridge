from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.project_evaluation import ProjectEvaluation
from app.models.project_submission import ProjectSubmission
from app.schemas.project_evaluation import ProjectEvaluationCreate
from app.services.project_ai_service import evaluate_project as ai_evaluate_project_service
from app.models.project import Project



router = APIRouter(
    prefix="/project-evaluations",
    tags=["Project Evaluations"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{submission_id}")
def evaluate_project(
    submission_id: int,
    data: ProjectEvaluationCreate,
    db: Session = Depends(get_db)
):
    submission = db.query(ProjectSubmission).filter(
        ProjectSubmission.id == submission_id
    ).first()

    if not submission:
        return {
            "message": "Project submission not found"
        }

    evaluation = ProjectEvaluation(
        submission_id=submission_id,
        implementation_score=data.implementation_score,
        project_understanding_score=data.project_understanding_score,
        feedback=data.feedback
    )

    db.add(evaluation)

    submission.status = "Evaluated"

    db.commit()
    db.refresh(evaluation)

    return {
        "message": "Project evaluated",
        "evaluation_id": evaluation.id,
        "submission_id": evaluation.submission_id,
        "implementation_score": evaluation.implementation_score,
        "project_understanding_score": evaluation.project_understanding_score,
        "feedback": evaluation.feedback
    }

@router.post("/ai/{submission_id}")
def ai_evaluate_project(
    submission_id: int,
    db: Session = Depends(get_db)
):
    submission = db.query(ProjectSubmission).filter(
        ProjectSubmission.id == submission_id
    ).first()

    if not submission:
        return {"message": "Submission not found"}

    project = db.query(Project).filter(
        Project.id == submission.project_id
    ).first()

    if not project:
        return {"message": "Project not found"}

    result = ai_evaluate_project_service(
       project.description,
       submission.submission_text or ""
    )
    evaluation = ProjectEvaluation(
    submission_id=submission.id,
    implementation_score=result["implementation_score"],
    project_understanding_score=result["project_understanding_score"],
    feedback=result["feedback"]
)

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
        

    return {
        "submission_id": submission_id,
        "ai_evaluation": result
    }

    return {
        "submission_id": submission.id,
        "ai_evaluation": result
    }