from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import user_schema  
from app.db.repositories import users_repo
from app.db.session import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Create a new user
@router.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return users_repo.create_user(db=db, user=user)

# Get a user by id
@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users_repo.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update user by id
@router.put("/{user_id}", response_model=user_schema.User)
def update_user(user_id: int, user_update: user_schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = users_repo.update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Delete user by id
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users_repo.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Get all users
@router.get("/", response_model=List[user_schema.User])
def read_all_users(db: Session = Depends(get_db)):
    return users_repo.get_all_users(db=db)
