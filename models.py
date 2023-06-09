from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List
import datetime



class Birthday(BaseModel):
    year: int
    month: int
    day: int

class UserInfo(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    username: str
    surname: Optional[str]
    birthdate: Birthday = Field(..., description="Date of birth")
    email: str
    password: str


class UpdateUserInfo(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    surname: Optional[str]
    birthdate: Optional[Birthday] = Field(..., description="Date of birth")
    email: Optional[str]
    password: Optional[str]


def check_Birthday(birthdate: Birthday):
    current_year = datetime.datetime.now().year

    if birthdate.year < 1940 or birthdate.year > current_year:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid year"
        )

    if birthdate.year > current_year - 18:
        raise HTTPException(
            status_code=400,
            detail="Your age is less than 18"
        )

    if birthdate.month < 1 or birthdate.month > 12:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid month"
        )

    if birthdate.day < 1 or birthdate.day > 31:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid day"
        )


