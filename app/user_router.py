"""
Router for User 
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Union, Optional, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.orm import User, Phone
from app.database.dbengine import get_db

router = APIRouter(prefix='',tags=['app'])

class UserCreate(BaseModel):
    name: str
    fullname: str
    phone_numbers: Optional[List[str]] = None


@router.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return {"id": user.id, "name": user.name, "fullname": user.fullname, "phone_numbers": user.phone_numbers}
    except BaseException as e: 
        print(e)
        return {"message": "Not found"}


@router.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
 
    db_user = User(name=user.name, fullname=user.fullname)
    for phone_number in user.phone_numbers:
        new_phone = Phone(phone_number=phone_number)
        db_user.phone_numbers.append(new_phone)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "name": db_user.name, "fullname": db_user.fullname, "phone_numbers": db_user.phone_numbers}
 
@router.put("/users/{user_id}")
async def update_user(user_id: int, user: dict, db: Session = Depends(get_db)):
    # Retrieve the user from the database
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )

   # Update the user's properties
    for key in user.keys():
        if key == 'phone_numbers':
            for phone_number in user.get("phone_numbers"):
                new_phone = Phone(phone_number=phone_number)
                db_user.phone_numbers.append(new_phone)
            continue
        db_user.__setattr__(key, user[key])

    # Commit the changes to the database
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "name": db_user.name, "fullname": db_user.fullname, "phone_numbers": db_user.phone_numbers}
 
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(db_user)
    db.commit()

    return {"message": "User deleted successfully"}

@router.get("/users/")
async def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": [{"id": user.id, "name": user.name, "fullname": user.fullname, "phone_numbers": user.phone_numbers} for user in users]}

@router.get("/phone_numbers/")
async def list_phone(db: Session = Depends(get_db)):
    phones = db.query(Phone).all()
    return {"phone_numbers": [{"id": phone.id, "phone_number": phone.phone_number, "user": phone.user} for phone in phones]}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
