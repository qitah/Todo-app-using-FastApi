from typing import Annotated, Optional
from fastapi import Query
from pydantic import BaseModel, EmailStr
from fastapi import Query
from pydantic import BaseModel, field_validator
from datetime import datetime

from app.models.todos_model import Task


class CreateTodo(BaseModel):
    title: str
    user_id: int

class createTask(BaseModel):
    title: str
    todo_id: int
    due_date: str = Query(..., regex=r"^\d{4}-\d{2}-\d{2}$ || \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

    @field_validator("due_date", mode="before")
    def format_due_date(cls, value):
        if value:
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            return value
    
    class Config:
        from_attributes = True

class GetTask(BaseModel):
    title: str
    todo_id: int
    due_date: str
    is_done: bool

    @field_validator("due_date", mode="before")
    def format_due_date(cls, value):
        if value:
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            return value
    
    class Config:
        from_attributes = True

class updateTask(BaseModel):
    title: Optional[str] = None
    is_done: Optional[bool] = None
    due_date: Annotated[str  | None, Query(..., regex=r"^\d{4}-\d{2}-\d{2}$ || \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")] = None 

    @field_validator("due_date", mode="before")
    def format_due_date(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value

class ListTodoTasks(BaseModel):
    id: int
    title: str
    user_id: int
    tasks: list[GetTask] = []