from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.topic_assessment import TopicAssessment
from app.models.user import User
from app.models.skill import Skill
from app.models.question import Question
from app.schemas.question import QuestionResponse
from app.schemas.topic_assessment import TopicQuestionsResponse
from app.models.topic_assessment_answer import TopicAssessmentAnswer
from app.schemas.topic_assessment_answer import TopicAssessmentAnswerCreate


router = APIRouter(
    prefix="/topic-assessments",
    tags=["Topic Assessments"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/start/{user_id}/{skill_id}")
def start_topic_assessment(
    user_id: int,
    skill_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {
            "message": "User not found"
        }

    skill = db.query(Skill).filter(
        Skill.id == skill_id
    ).first()

    if not skill:
        return {
            "message": "Skill not found"
        }

    assessment = TopicAssessment(
        user_id=user_id,
        skill_id=skill_id
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return {
        "message": "Topic assessment started",
        "assessment_id": assessment.id,
        "user_id": user_id,
        "skill_id": skill_id,
        "skill": skill.name,
        "score": 0
    }


@router.get(
    "/{assessment_id}/questions",
    response_model=TopicQuestionsResponse
)
def get_topic_assessment_questions(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    assessment = db.query(TopicAssessment).filter(
        TopicAssessment.id == assessment_id
    ).first()

    if not assessment:
        return {
            "message": "Topic assessment not found"
        }

    questions = db.query(Question).filter(
        Question.skill_id == assessment.skill_id
    ).all()

    return {
        "assessment_id": assessment_id,
        "skill_id": assessment.skill_id,
        "questions": questions
    }

@router.post("/{assessment_id}/answer")
def submit_topic_answer(
    assessment_id: int,
    answer: TopicAssessmentAnswerCreate,
    db: Session = Depends(get_db)
):
    assessment = db.query(TopicAssessment).filter(
        TopicAssessment.id == assessment_id
    ).first()

    if not assessment:
        return {
            "message": "Topic assessment not found"
        }

    question = db.query(Question).filter(
        Question.id == answer.question_id,
        Question.skill_id == assessment.skill_id
    ).first()

    if not question:
        return {
            "message": "Question not found for this assessment"
        }

    new_answer = TopicAssessmentAnswer(
        assessment_id=assessment_id,
        question_id=answer.question_id,
        selected_answer=answer.selected_answer.upper()
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return {
        "message": "Topic assessment answer saved",
        "answer_id": new_answer.id,
        "assessment_id": assessment_id,
        "question_id": answer.question_id,
        "selected_answer": new_answer.selected_answer
    }

@router.get("/{assessment_id}/result")
def get_topic_assessment_result(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    assessment = db.query(TopicAssessment).filter(
        TopicAssessment.id == assessment_id
    ).first()

    if not assessment:
        return {
            "message": "Topic assessment not found"
        }

    answers = db.query(TopicAssessmentAnswer).filter(
        TopicAssessmentAnswer.assessment_id == assessment_id
    ).all()

    total_questions = db.query(Question).filter(
        Question.skill_id == assessment.skill_id
    ).count()

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

    assessment.score = score

    db.commit()
    db.refresh(assessment)

    return {
        "assessment_id": assessment_id,
        "skill_id": assessment.skill_id,
        "total_questions": total_questions,
        "answered_questions": len(answers),
        "correct_answers": correct_answers,
        "score": score
    }