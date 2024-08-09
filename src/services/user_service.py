from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.db.db import SessionLocal
from src.models.user import User
from src.auth.auth import get_password_hash, verify_password, create_access_token

def create_user_service(user_data):
    hashed_password = get_password_hash(user_data.password)
    db_user = User(username=user_data.username, hashed_password=hashed_password)
    with SessionLocal() as db:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"username": db_user.username, "message": "User created successfully"}

def authenticate_user(form_data):
    username = form_data.username
    password = form_data.password
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
