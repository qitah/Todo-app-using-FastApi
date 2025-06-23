from fastapi import FastAPI

from app.helpers import jwt_helper
from app.models import users_model
from app.db.session import engine
from app.api import users
from app.api import todos
from datetime import datetime, timedelta, timezone
import os
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.helpers.password_helper import verify_password
from app.models.users_model import User
from app.schemas.user_schema import ShowUser, UserLogin
from app.helpers.jwt_helper import ACCESS_TOKEN_EXPIRE_MINUTES, Token, authenticate_user, create_access_token

users_model.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(todos.router)
app.include_router(jwt_helper.router)
 
@app.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")