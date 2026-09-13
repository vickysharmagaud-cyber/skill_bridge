from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.learning_content import LearningContent
from app.schemas.learning_content import LearningContentCreate


router = APIRouter(
    prefix="/learning",
    tags=["Learning"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_learning_content(
    data: LearningContentCreate,
    db: Session = Depends(get_db)
):
    new_content = LearningContent(
        skill_id=data.skill_id,
        title=data.title,
        content=data.content,
        order=data.order
    )

    db.add(new_content)
    db.commit()
    db.refresh(new_content)

    return {
        "message": "Learning content created",
        "id": new_content.id,
        "skill_id": new_content.skill_id,
        "title": new_content.title,
        "order": new_content.order
    }

@router.get("/{skill_id}")
def get_learning_content(
    skill_id: int,
    db: Session = Depends(get_db)
):
    contents = db.query(LearningContent).filter(
        LearningContent.skill_id == skill_id
    ).order_by(LearningContent.order).all()

    if not contents:
        return {
            "message": "No learning content found"
        }

    return {
        "skill_id": skill_id,
        "contents": contents
    }