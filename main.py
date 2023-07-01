from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID
from models import UserInfo, UpdateUserInfo, CheckInfo
import datetime


app = FastAPI()


check = CheckInfo()


db: List[UserInfo] = []


@app.get("/")
def fetch_all_users():
    return db


@app.get("/api/auth/{user_id}")
def fetch_users(user_id: UUID):
    for user in db: 
        if user.id == user_id:
            return user
        raise HTTPException(
            status_code=404,
            detail=f"{user_id} not found"
        )


@app.post("/api/auth/sign_up")
def create_acc(user: UserInfo):
    current_year = datetime.datetime.now().year

    for existing_user in db:
        if existing_user.email == user.email:
            return f"{user.email} is already in use"
        if existing_user.id == user.id:
            return f"You can't give the same id"
    if not check.is_valid_phone_number(user.phone_number):
        return f"Invalid phone number: {user.phone_number}"
    check.check_Birthday(user.birthdate)
    db.append(user)
    return f"Your date of birth is: {user.birthdate.year}-{user.birthdate.month}-{user.birthdate.day}! Your Age is {current_year - user.birthdate.year}"


@app.put("/api/auth/{user_id}/edit")
def edit_info(user_id: UUID, update_user: UpdateUserInfo):
    user = next((u for u in db if u.id == user_id), None)
    if user:
        updated_fields = update_user.dict(exclude_unset=True)
        for field, value in updated_fields.items():
            setattr(user, field, value)
        check.check_Birthday(update_user.birthdate)
        if not check.is_valid_phone_number(user.phone_number):
            return f"Invalid phone number: {user.phone_number}"
        return "Edited"
    raise HTTPException(
        status_code=404,
        detail=f"User with id: {user_id} not found."
    )



@app.delete("/api/auth/{user_id}/delete")
def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return "Succesfuly Deleted"
        raise HTTPException(
            status_code=404,
            detail=f"User with id: {user_id} does not found."
        )

