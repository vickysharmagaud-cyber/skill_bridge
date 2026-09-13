from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.assessment import Assessment
from app.models.user import User
from app.models.question import Question
from app.models.assessment_answer import AssessmentAnswer
from app.schemas.assessment import AnswerCreate
from app.models.skill import Skill
from datetime import datetime


router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/start/{user_id}")
def start_assessment(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {
            "message": "User not found"
        }

    assessment = Assessment(
        user_id=user_id
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return {
        "message": "Assessment started",
        "assessment_id": assessment.id,
        "user_id": assessment.user_id,
        "started_at": assessment.started_at
    }

@router.get("/{assessment_id}/questions")
def get_assessment_questions(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id
    ).first()

    if not assessment:
        return {
            "message": "Assessment not found"
        }

    questions = db.query(Question).all()

    return {
        "assessment_id": assessment_id,
        "questions": questions
    }

@router.post("/{assessment_id}/answer")
def submit_answer(
    assessment_id: int,
    answer: AnswerCreate,
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id
    ).first()

    if not assessment:
        return {
            "message": "Assessment not found"
        }

    new_answer = AssessmentAnswer(
        assessment_id=assessment_id,
        question_id=answer.question_id,
        selected_answer=answer.selected_answer.upper()
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return {
        "message": "Answer saved",
        "answer_id": new_answer.id,
        "assessment_id": assessment_id,
        "question_id": answer.question_id,
        "selected_answer": new_answer.selected_answer
    }

@router.get("/{assessment_id}/result")
def get_assessment_result(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id
    ).first()

    if not assessment:
        return {
            "message": "Assessment not found"
        }

    answers = db.query(AssessmentAnswer).filter(
        AssessmentAnswer.assessment_id == assessment_id
    ).all()

    total_questions = db.query(Question).count()

    correct_answers = 0

    for answer in answers:
        question = db.query(Question).filter(
            Question.id == answer.question_id
        ).first()

        if question and answer.selected_answer.upper() == question.correct_answer.upper():
            correct_answers += 1

    score = 0

    if total_questions > 0:
        score = (correct_answers / total_questions) * 100

    return {
        "assessment_id": assessment_id,
        "total_questions": total_questions,
        "answered_questions": len(answers),
        "correct_answers": correct_answers,
        "score": score
    }

@router.get("/{assessment_id}/skill-results")
def get_skill_results(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id
    ).first()

    if not assessment:
        return {
            "message": "Assessment not found"
        }

    answers = db.query(AssessmentAnswer).filter(
        AssessmentAnswer.assessment_id == assessment_id
    ).all()

    skill_results = {}

    for answer in answers:
        question = db.query(Question).filter(
            Question.id == answer.question_id
        ).first()

        if not question:
            continue

        skill = db.query(Skill).filter(
            Skill.id == question.skill_id
        ).first()

        if not skill:
            continue

        skill_name = skill.name

        if skill_name not in skill_results:
            skill_results[skill_name] = {
                "total": 0,
                "correct": 0
            }

        skill_results[skill_name]["total"] += 1

        if answer.selected_answer.upper() == question.correct_answer.upper():
            skill_results[skill_name]["correct"] += 1

    result = []

    for skill_name, data in skill_results.items():

        score = (data["correct"] / data["total"]) * 100

        result.append({
            "skill": skill_name,
            "total_questions": data["total"],
            "correct_answers": data["correct"],
            "score": score
        })

    return {
        "assessment_id": assessment_id,
        "skill_results": result
    }

@router.post("/{assessment_id}/complete")
def complete_assessment(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id
    ).first()

    if not assessment:
        return {
            "message": "Assessment not found"
        }

    if assessment.completed_at is not None:
        return {
            "message": "Assessment already completed",
            "completed_at": assessment.completed_at
        }

    assessment.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(assessment)

    return {
        "message": "Assessment completed",
        "assessment_id": assessment.id,
        "completed_at": assessment.completed_at
    }