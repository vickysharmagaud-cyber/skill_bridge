from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.roadmap import Roadmap
from app.models.user import User
from app.models.skill import Skill
from app.models.assessment import Assessment
from app.models.assessment_answer import AssessmentAnswer
from app.models.question import Question


router = APIRouter(
    prefix="/roadmaps",
    tags=["Roadmaps"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/generate/{user_id}")
def generate_roadmap(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {
            "message": "User not found"
        }

    skills = db.query(Skill).all()

    roadmap = []

    for index, skill in enumerate(skills, start=1):

        existing = db.query(Roadmap).filter(
            Roadmap.user_id == user_id,
            Roadmap.skill_id == skill.id
        ).first()

        if existing:
            continue

        new_roadmap = Roadmap(
            user_id=user_id,
            skill_id=skill.id,
            status="Not Started",
            priority=index
        )

        db.add(new_roadmap)

        roadmap.append({
            "skill": skill.name,
            "status": "Not Started",
            "priority": index
        })

    db.commit()

    return {
        "message": "Roadmap generated",
        "user_id": user_id,
        "roadmap": roadmap
    }

@router.post("/generate/{user_id}")
def generate_roadmap(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {
            "message": "User not found"
        }

    # Get the user's latest assessment
    assessment = db.query(Assessment).filter(
        Assessment.user_id == user_id
    ).order_by(Assessment.id.desc()).first()

    if not assessment:
        return {
            "message": "No assessment found for this user"
        }

    # Get all answers from the assessment
    answers = db.query(AssessmentAnswer).filter(
        AssessmentAnswer.assessment_id == assessment.id
    ).all()

    skill_scores = {}

    # Calculate score for each skill
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

        if skill.id not in skill_scores:
            skill_scores[skill.id] = {
                "skill": skill.name,
                "total": 0,
                "correct": 0
            }

        skill_scores[skill.id]["total"] += 1

        if answer.selected_answer.upper() == question.correct_answer.upper():
            skill_scores[skill.id]["correct"] += 1

    # Delete old roadmap for this user
    db.query(Roadmap).filter(
        Roadmap.user_id == user_id
    ).delete()

    roadmap = []

    # Sort weakest skills first
    sorted_skills = sorted(
        skill_scores.values(),
        key=lambda x: (
            x["correct"] / x["total"]
            if x["total"] > 0 else 0
        )
    )

    for priority, data in enumerate(sorted_skills, start=1):

        score = (
            data["correct"] / data["total"]
        ) * 100 if data["total"] > 0 else 0

        skill_id = next(
            skill_id
            for skill_id, value in skill_scores.items()
            if value["skill"] == data["skill"]
        )

        new_roadmap = Roadmap(
            user_id=user_id,
            skill_id=skill_id,
            status="Not Started",
            priority=priority
        )

        db.add(new_roadmap)

        roadmap.append({
            "skill": data["skill"],
            "score": score,
            "priority": priority,
            "status": "Not Started"
        })

    db.commit()

    return {
        "message": "Personalized roadmap generated",
        "user_id": user_id,
        "roadmap": roadmap
    }

@router.get("/{user_id}")
def get_roadmap(
    user_id: int,
    db: Session = Depends(get_db)
):
    roadmap = db.query(Roadmap).filter(
        Roadmap.user_id == user_id
    ).order_by(Roadmap.priority).all()

    if not roadmap:
        return {
            "message": "No roadmap found"
        }

    result = []

    for item in roadmap:

        skill = db.query(Skill).filter(
            Skill.id == item.skill_id
        ).first()

        result.append({
            "roadmap_id": item.id,
            "skill": skill.name if skill else None,
            "status": item.status,
            "priority": item.priority
        })

    return {
        "user_id": user_id,
        "roadmap": result
    }

@router.put("/{roadmap_id}/status")
def update_roadmap_status(
    roadmap_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    roadmap_item = db.query(Roadmap).filter(
        Roadmap.id == roadmap_id
    ).first()

    if not roadmap_item:
        return {
            "message": "Roadmap item not found"
        }

    roadmap_item.status = status

    db.commit()
    db.refresh(roadmap_item)

    return {
        "message": "Roadmap status updated",
        "roadmap_id": roadmap_item.id,
        "status": roadmap_item.status
    }