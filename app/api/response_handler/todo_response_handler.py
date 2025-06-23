from starlette import status
from app.models.todos_model import Task, Todo
from app.models.users_model import User
from app.schemas import todo_schema


def create_todo_list(request: todo_schema.CreateTodo, response, db):
    user_todo_list = db.query(Todo).filter(Todo.user_id==request.user_id).first()
    if user_todo_list:
        response.status_code = status.HTTP_409_CONFLICT
        return {
            'message': "User todo list already exists",
            'status_code': 409,
            'error': 'CONFLICT'
        }
    
    todo = Todo(title=request.title, user_id=request.user_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
        'message': "success",
        'status_code': 201,
        'status': 'Success',
        'data': {
            'id': todo.id,
            'title': todo.title
        }
    }

def create_todo_task(request: todo_schema.createTask, response, db):
    task = Task(
        title=request.title,
        todo_id=request.todo_id,
        due_date=request.due_date
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return {
        'message': "success",
        'status_code': 201,
        'status': 'Success',
        'data': {
            'id': task.id,
            'title': task.title
        }
    }

def get_todo_list_with_tasks(todo_id: int, response, db):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "Todo list not found",
            'status_code': 404,
            'error': 'NOT FOUND'
        }
    
    tasks = db.query(Task).filter(Task.todo_id == todo_id).all()
    return {
        'message': "success",
        'status_code': 200,
        'status': 'Success',
        'data': todo_schema.ListTodoTasks(
            id=todo.id,
            title=todo.title,
            user_id=todo.user_id,
            tasks=[todo_schema.GetTask(
                id=task.id,
                title=task.title,
                todo_id=task.todo_id,
                due_date=task.due_date,
                is_done=task.is_done
            ) for task in tasks]
        )
    }

def delete_todo_list(todo_id: int, response, db):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "Todo list not found",
            'status_code': 404,
            'error': 'NOT FOUND'
        }
    
    db.delete(todo)
    db.commit()
    return {
        'message': "todo_list deleted successfully",
        'status_code': 204,
        'status': 'Success',
        'data': None
    }

def update_todo_task(todo_id: int, task_id:int, request: todo_schema.updateTask, response, db):
    task = db.query(Task).filter(Task.id == task_id, Task.todo_id == todo_id).first()
    if not task:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "Task not found",
            'status_code': 404,
            'error': 'NOT FOUND'
        }
    updated_data = request.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return {
        'message': "Task updated successfully",
        'status_code': 200,
        'status': 'Success',
        'data': todo_schema.GetTask(title=task.title, todo_id=task.todo_id, due_date=task.due_date, is_done=task.is_done)
    }

def share_to_do_list_with_user(user_id: int, todo_id: int, response, db):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "User not found",
            'status_code': 404,
            'error': 'NOT FOUND'
        }
    
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "Todo list not found",
            'status_code': 404,
            'error': 'NOT FOUND'
        }
    user.shared_lists.append(todo)
    db.commit()

    return {
        'message': "Todo list shared successfully",
        'status_code': 201,
        'status': 'Success',
    }

def get_shared_todo_list(user_id: int, response, db):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "User not found",
            'status_code': 404,
            'error': 'NOT FOUND'
        }
    
    shared_todo_lists = db.query(Todo).filter(Todo.shared_with.any(id=user_id)).all()
    if len(shared_todo_lists) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "No shared todo lists found",
            'status_code': 404,
            'error': 'NOT FOUND'
        }
    
    return {
        'message': "success",
        'status_code': 200,
        'status': 'Success',
        'data': [
            {
                'id': todo.id,
                'title': todo.title,
                'user_id': todo.user_id
            } for todo in shared_todo_lists
        ]
    }