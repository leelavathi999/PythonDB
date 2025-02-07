from sqlalchemy.orm import Session
from app.db.models.item_model import Item
from app.schemas.item_schema import ItemCreate, ItemUpdate, Item as ItemSchema

# Create a new item
def create_item(db: Session, item: ItemCreate, user_id: int):
    db_item = Item(name=item.name, description=item.description, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Get items by user ID
def get_items_by_user(db: Session, user_id: int):
    return db.query(Item).filter(Item.owner_id == user_id).all()

# Update item by item ID
def update_item(db: Session, item_id: int, item_update: ItemUpdate):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        return None
    db_item.name = item_update.name or db_item.name
    db_item.description = item_update.description or db_item.description

    db.commit()
    db.refresh(db_item)
    return db_item

# Delete item by item ID
def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

# Get all items
def get_all_items(db: Session):
    return db.query(Item).all()
