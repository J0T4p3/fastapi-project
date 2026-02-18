from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_duno.database import get_session
from fastapi_duno.models import User
from fastapi_duno.schemas import UserDB, Userlist, UserPublic, UserSchema

app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

database = []


@app.get('/users', response_model=Userlist)
def get_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {'users': users}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user_by_id(user_id: int):
    if user_id < 0 or user_id > len(database):
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail=f'User {user_id} not found'
        )

    try:
        user: UserSchema = database[user_id - 1]
        return user
    except KeyError:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail=f'User {user_id} not found'
        )


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                HTTPStatus.CONFLICT, detail='Usernamed already registered'
            )
        if db_user.email == user.email:
            raise HTTPException(
                HTTPStatus.CONFLICT, detail='Email already registered'
            )

    db_user = User(
        username=user.username,
        password=user.password,
        email=user.email,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User {user_id} not found',
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User {user_id} not found',
        )

    try:
        del database[user_id - 1]
    except KeyError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User {user_id} not found',
        )
    return {'detail': f'User {user_id} deleted'}
