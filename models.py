from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UserInfo(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    username: str
    surname: Optional[str]
    age: int
    email: str
    password: str


class UpdateUserInfo(BaseModel):
    first_name: str
    last_name: str
    username: str
    surname: Optional[str]
    age: int
    email: str
    password: str