
from fastapi import Depends, APIRouter, Response
from app.api.response_handler import todo_response_handler
from app.db.session import get_db
from app.schemas import todo_schema
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/todos", tags=["todos"],)


@router.post("/", status_code=201, tags=['todos'])
def create_todo(request: todo_schema.CreateTodo, response: Response, db: Session = Depends(get_db)):
    return todo_response_handler.create_todo_list(request, response, db)


@router.get("/{todo_id}/tasks", status_code=200, tags=['todos']) 
def get_todo_list_with_tasks(todo_id: int, response: Response, db: Session = Depends(get_db)):
    return todo_response_handler.get_todo_list_with_tasks(todo_id, response, db)


@router.delete("/{todo_id}", status_code=204, tags=['todos'])
def delete_todo(todo_id: int, response: Response, db: Session = Depends(get_db)):
    return todo_response_handler.delete_todo_list(todo_id, response, db)

@router.post("/task", status_code=201)
def create_todo_task(request: todo_schema.createTask, response: Response, db: Session = Depends(get_db)):
    return todo_response_handler.create_todo_task(request, response, db)

@router.put("/{todo_id}/tasks/{task_id}", status_code=200)
def update_todo_task(todo_id: int, task_id:int, request: todo_schema.updateTask, response: Response, db: Session = Depends(get_db)):
    return todo_response_handler.update_todo_task(todo_id,task_id, request, response, db)


@router.post("/share-todo-list/", status_code=201, tags=['todos']) 
def share_todo_list(user_id: int, todo_id: int, response: Response, db: Session = Depends(get_db)):
    return todo_response_handler.share_to_do_list_with_user(user_id, todo_id, response, db)


@router.get("/shared-todo-list/{user_id}", status_code=200, tags=['todos'])
def get_shared_todo_list(user_id: int, response: Response, db: Session = Depends(get_db)):
    return todo_response_handler.get_shared_todo_list(user_id, response, db)