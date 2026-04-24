import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.database import User, get_db
from ..models.schemas import UserCreate, UserOut

router = APIRouter()


@router.post(
    "/users",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        preferences=json.dumps(payload.preferences) if payload.preferences else None,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserOut(
        user_id=user.id,
        message="User created successfully.",
    )


@router.get(
    "/users/{user_id}",
    summary="Get user details",
)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    preferences = None
    if user.preferences:
        try:
            preferences = json.loads(user.preferences)
        except (json.JSONDecodeError, TypeError):
            preferences = None

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "preferences": preferences,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }
