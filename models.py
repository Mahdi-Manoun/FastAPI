from fastapi import HTTPException
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional
import datetime, phonenumbers
from dateutil import parser


class Birthday(BaseModel):
    year: int
    month: int
    day: int

class UserInfo(BaseModel):
    id: UUID = uuid4()
    first_name: str
    last_name: str
    username: str
    surname: Optional[str]
    birthdate: Birthday = Field(..., description="Date of birth")
    phone_number: str
    email: str
    password: str


class UpdateUserInfo(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    surname: Optional[str]
    birthdate: Optional[Birthday] = Field(..., description="Date of birth")
    phone_number: Optional[str]
    email: Optional[str]
    password: Optional[str]


class CheckInfo:

    def __init__(self):
        self.errors = {
            "year": "Enter a valid year",
            "age": "Your age is less than 18",
            "month": "Enter a valid month",
            "day": "Enter a valid day",
            "dob": "Please, enter your date of birth",
        }

    def check_Birthday(self, birthdate: Birthday):

        current_date = datetime.date.today()
        date_of_birth = datetime.date(birthdate.year, birthdate.month, birthdate.day)


        if all(component == 0 for component in [birthdate.year, birthdate.month, birthdate.day]):
            raise ValueError(status_code=400, detail="Invalid birthdate")
        elif birthdate.year < 1940 or birthdate.year > current_date.year:
            error_type = "year"
        elif birthdate.year > current_date.year - 18:
            error_type = "age"
        elif birthdate.month < 1 or birthdate.month > 12:
            error_type = "month"
        elif birthdate.day < 1 or birthdate.day > 31:
            error_type = "day"
        elif any(component is None for component in [birthdate.year, birthdate.month, birthdate.day]):
            error_type = "dob"
        else:
            age = current_date - date_of_birth
            age_in_years = age.days / 365
            return round(age_in_years, 2)

        if error_type:
            raise HTTPException(status_code=400, detail=self.errors[error_type])

    
    def is_valid_phone_number(self, phone_number):
            parsed_number = phonenumbers.parse(phone_number)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError(
                    status_code=400, detail="Enter a valid phone number"
                )
            return f"You\'r phone number is {parsed_number}"
