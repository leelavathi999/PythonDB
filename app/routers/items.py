from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database
from app.repositories import items
router = APIRouter(
    prefix="/items",
    tags=["items"]
)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new item
@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, user_id: int, db: Session = Depends(get_db)):
    return items.create_item(db=db, item=item, user_id=user_id)

# Get items by user id
@router.get("/{user_id}", response_model=List[schemas.Item])
def get_items_by_user(user_id: int, db: Session = Depends(get_db)):
    return items.get_items_by_user(db=db, user_id=user_id)

# Update item by id
@router.put("/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = items.update_item(db=db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Delete item by id
@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = items.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

# Get all items
@router.get("/", response_model=List[schemas.Item])
def read_all_items(db: Session = Depends(get_db)):
    return items.get_all_items(db=db)
