from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.models.users_model import User
from app.db.session import get_db
from app.helpers import password_helper
from app.schemas import user_schema
from sqlalchemy import or_


def sign_up(request: user_schema.User, response, db):
    user = db.query(User).filter(or_(User.email == request.email, User.username == request.username)).first()
    if user:
        response.status_code = status.HTTP_409_CONFLICT
        return {
            'message': "User with this email or username already exists",
            'status_code': 409,
            'error': 'CONFLICT'
        }

    hash_password = password_helper.hash_password(request.password)
    new_user = User(username=request.username, email=request.email, password=hash_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        'message': "success",
        'status_code': 201,
        'status': 'Success',
        'data': {
            'id': new_user.id,
            'email': new_user.email
        }
    }


def login(request: user_schema.UserLogin, response, db):
    user: User = db.query(User).filter(User.username == request.username).first()
    if not user:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid username and/or password",
            'status_code': 403,
            'error': 'FORBIDDEN'
        }

    if not (password_helper.verify_password(request.password, user.password)):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid username and/or password",
            'status_code': 403,
            'error': 'FORBIDDEN'
        }
    return {
        'message': 'Success',
        'status_code': 200,
        'data': {
            'email': user.username,
            'id': user.id
        },
    }


def show(user_id: int, response, db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.id == user_id).first()
    if not user_id:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "User not found",
            'status_code': 404,
            'error': 'NOT_FOUND'
        }
    return {
        'message': 'Success',
        'status_code': 200,
        'data': user_schema.ShowUser(
            id=user_id.id,
            username=user_id.username,
            email=user_id.email,
            crated_at=user_id.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=user_id.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        )
    }


    
