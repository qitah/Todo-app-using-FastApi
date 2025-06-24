from typing import Annotated
from fastapi import Depends, APIRouter, Response
from app.api.response_handler import user_response_handler
from app.db.session import get_db
from app.helpers.jwt_helper import get_current_user
from app.models.users_model import User
from app.schemas import user_schema
from sqlalchemy.orm import Session



router = APIRouter(prefix="/api/users", tags=["users"],)


@router.post('/sign_up', status_code=201, tags=['users'])
def sign_up(request: user_schema.User, response: Response, db: Session = Depends(get_db)):
    return user_response_handler.sign_up(request, response, db)


@router.post('/sign_in', status_code=200, tags=['users'])
def login(request: user_schema.UserLogin, response: Response, db: Session = Depends(get_db)):
    return user_response_handler.login(request, response, db)


@router.get("/{user_id}", status_code=200, tags=['users'],  )
def show(user_id: int, response: Response, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return user_response_handler.show(user_id, response, db)