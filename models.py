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
    current_date = datetime.date.today()
    date_of_birth = datetime.date(birthdate.year, birthdate.month, birthdate.day)

    if birthdate.year < 1940 or birthdate.year > current_date.year:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid year"
        )
    elif birthdate.year > current_date.year - 18:
        raise HTTPException(
            status_code=400,
            detail="Your age is less than 18"
        )
    elif birthdate.month < 1 or birthdate.month > 12:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid month"
        )
    elif birthdate.day < 1 or birthdate.day > 31:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid day"
        )
    elif any(component is None for component in [birthdate.year, birthdate.month, birthdate.day]):
        raise HTTPException(
            status_code=400,
            detail="Please, enter your date of birth"
        )
    else:
        age = current_date - date_of_birth
        age_in_years = age.days / 365
        return round(age_in_years, 2)


