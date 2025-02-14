from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, User
from app.auth import get_current_user

router = APIRouter()

@router.get("/users/me")
def get_user_details(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve current logged-in user's details"""
    db_user = db.query(User).filter(User.username == user["username"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email
    }
