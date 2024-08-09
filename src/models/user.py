from sqlalchemy import Column, Integer, String
from src.models.base import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class UserCreate(BaseModel):
    username: str
    password: str
