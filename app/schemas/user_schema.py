from datetime import datetime
from fastapi import Query
from pydantic import BaseModel, EmailStr, field_validator
from typing import Union


class User(BaseModel):
    username: str
    email: EmailStr
    password: str = Query(min_length=4)

class UserLogin(BaseModel):
    username: str
    password: str = Query(min_length=4)

class ShowUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    updated_at: str

        
    @field_validator("updated_at", mode="before")
    def format_updated_at(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value
    

