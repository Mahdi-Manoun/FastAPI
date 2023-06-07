from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID
from models import UserInfo, UpdateUserInfo


app = FastAPI()


db: List[UserInfo] = []


@app.get("/facebook.com")
def fetch_all_users():
    return db

@app.get("/facebook.com/{username}")
def fetch_users(username: str):
    for user in db: 
        if user.username == username:
            return user
        raise HTTPException(
            status_code=404,
            detail=f"{username} not found"
        )

@app.post("/facebook.com/sign_up")
def create_acc(user: UserInfo):
    db.append(user)


@app.put("/facebook.com/{user_id}")
def edit_info(update_user: UpdateUserInfo, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user.first_name != update_user.first_name:
                user.first_name = update_user.first_name
            if user.last_name != update_user.last_name:
                user.last_name = update_user.last_name
            if user.username != update_user.username:
                user.username = update_user.username
            if user.surname != update_user.surname:
                user.surname = update_user.surname
            if user.age != update_user.age:
                user.age = update_user.age
            if user.email != update_user.email:
                user.email = update_user.email
            if user.password != update_user.password:
                user.password = update_user.password
            return "Edited"
        raise HTTPException(
            status_code=404,
            detail=f"User with id: {user_id} does not found."
        )


@app.delete("/facebook.com/{user_id}")
def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return "Succesfuly Deleted"
        raise HTTPException(
            status_code=404,
            detail=f"User with id: {user_id} does not found."
        )
