from fastapi import FastAPI
from app.database.database import engine, Base
from app.models.user import User
from app.models.skill import Skill
from app.models.question import Question
from app.models.assessment import Assessment
from app.models.assessment_answer import AssessmentAnswer
from app.models.roadmap import Roadmap
from app.models.learning_content import LearningContent
from app.models.topic_assessment import TopicAssessment
from app.models.topic_assessment_answer import TopicAssessmentAnswer
from app.models.project import Project
from app.models.project_submission import ProjectSubmission
from app.models.project_evaluation import ProjectEvaluation
from app.models.project_viva import ProjectViva
from app.services.groq_service import ask_groq
from fastapi.middleware.cors import CORSMiddleware

from app.routes.user import router as user_router
from app.routes.question import router as question_router
from app.routes.assessment import router as assessment_router
from app.routes.roadmap import router as roadmap_router
from app.routes.learning_content import router as learning_router
from app.routes.topic_assessment import router as topic_assessment_router
from app.routes.project import router as project_router
from app.routes.project_submission import router as project_submission_router
from app.routes.project_evaluation import router as project_evaluation_router
from app.routes.project_viva import router as project_viva_router

app = FastAPI(title="SkillBridge AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(question_router)
app.include_router(assessment_router)
app.include_router(roadmap_router)
app.include_router(learning_router)
app.include_router(topic_assessment_router)
app.include_router(project_router)
app.include_router(project_submission_router)
app.include_router(project_evaluation_router)
app.include_router(project_viva_router)
@app.get("/")
def home():
    return {
        "message": "Welcome to SkillBridge AI Backend"
    }


@app.get("/test-db")
def test_db():
    try:
        with engine.connect():
            return {
                "status": "success",
                "message": "Database connected successfully"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/test-groq")
def test_groq():
    response = ask_groq("Say hello to SkillBridge AI in one sentence.")
    return {"response": response}