from sqlalchemy.orm import Session
from . import models, schemas , security

# Create a new user
def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get a user by id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# update user by id
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    if user_update.name:
        db_user.name = user_update.name
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = security.hash_password(user_update.password)  

    db.commit()
    db.refresh(db_user)
    return db_user

# delete user by id
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

# Get all users
def get_all_users(db: Session):
    return db.query(models.User).all()


# Create a new item
def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(name=item.name, description=item.description, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Get items by user id
def get_items_by_user(db: Session, user_id: int):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).all()

# udate item by item_id
def update_item(db: Session, item_id: int, item_update: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return None
    db_item.name = item_update.name or db_item.name
    db_item.description = item_update.description or db_item.description

    db.commit()
    db.refresh(db_item)
    return db_item

# delete item by item_id
def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

# Get all items
def get_all_items(db: Session):
    return db.query(models.Item).all()
