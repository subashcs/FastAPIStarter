
from fastapi import FastAPI, Depends
from typing import Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.orm.user import User
from app.database.dbengine import get_db

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    fullname: str
    address: int


@app.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return {"id": user.id, "name": user.name}


@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "name": db_user.name}


@app.get("/users/")
async def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": [{"id": user.id, "name": user.name} for user in users]}


@app.get("/")
def read_root():
    return {"Hello": "Subash"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
