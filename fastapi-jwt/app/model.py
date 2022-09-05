from email.policy import default
from fastapi import File
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from sqlmodel import Field
from enum import Enum
from pydantic import EmailStr
from uuid import UUID

from enum import Enum

from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID,uuid4
from beanie import Document
from pydantic import Field , EmailStr


class UserSchema(BaseModel):
    fullname : str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: str = Field(...)

    class Config:
       
        schema_extra = {
            "example": {
                "fullname": "Joy Joe",
                "email": "joy@x.com",
                "password": "weakpassword",
                "role":"admin"
            }
        }

    
class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "joy@x.com",
                "password": "weakpassword"
            }
        }


class StudentSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    course_of_study: str = Field(...)
    year: int = Field(..., gt=0, lt=9)
    gpa: float = Field(..., le=4.0)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources engineering",
                "year": "2",
                "gpa": "3.0"
            }
        }





class UpdateStudentModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    course_of_study: Optional[str]
    year: Optional[int]
    gpa: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources and environmental engineering",
                "year": "4",
                "gpa": "4.0"
            }
        }


def response_model(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def error_response_model(error, code, message):
    return {"error": error, "code": code, "message": message}

