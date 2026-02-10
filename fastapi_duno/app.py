from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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


@app.get('/users', status_code=HTTPStatus.OK, response_model=Userlist)
def get_users():
    return {'users': database}


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
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)
    return user_with_id


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
