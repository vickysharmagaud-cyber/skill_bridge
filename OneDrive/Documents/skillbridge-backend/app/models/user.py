from sqlalchemy import Column, Integer, String
from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    education = Column(String(100))
    branch = Column(String(100))
    year = Column(Integer)
    preferred_language = Column(String(50), default="English")
    career_goal = Column(String(100))
    