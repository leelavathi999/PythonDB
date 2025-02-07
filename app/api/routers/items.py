from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import item_schema
from app.db.repositories import items_repo
from app.db.session import get_db

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

# Create a new item
@router.post("/", response_model=item_schema.Item)
def create_item(item: item_schema.ItemCreate, user_id: int, db: Session = Depends(get_db)):
    return items_repo.create_item(db=db, item=item, user_id=user_id)

# Get items by user id
@router.get("/{user_id}", response_model=List[item_schema.Item])
def get_items_by_user(user_id: int, db: Session = Depends(get_db)):
    return items_repo.get_items_by_user(db=db, user_id=user_id)

# Update item by id
@router.put("/{item_id}", response_model=item_schema.Item)
def update_item(item_id: int, item_update: item_schema.ItemUpdate, db: Session = Depends(get_db)):
    db_item = items_repo.update_item(db=db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Delete item by id
@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = items_repo.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

# Get all items
@router.get("/", response_model=List[item_schema.Item])
def read_all_items(db: Session = Depends(get_db)):
    return items_repo.get_all_items(db=db)
