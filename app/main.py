from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from typing import List
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# Get a user by id
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# update user by id
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# delete user by id
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


# Get all users
@app.get("/users/", response_model=List[schemas.User])
def read_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db=db)

# Create a new item
@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item, user_id=user_id)

# Get items by user id
@app.get("/items/{user_id}", response_model=List[schemas.Item])
def get_items_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_items_by_user(db=db, user_id=user_id)

# update items by item_id
@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db=db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# delete items by item_id
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


# Get all items
@app.get("/items/", response_model=List[schemas.Item])
def read_all_items(db: Session = Depends(get_db)):
    return crud.get_all_items(db=db)
