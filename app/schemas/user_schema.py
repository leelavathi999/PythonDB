from pydantic import BaseModel
from typing import List, Optional
from app.schemas.item_schema import Item  # ✅ Added missing import

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    items: List[Item] = []  

    class Config:
        orm_mode = True
