import datetime
from http import HTTPStatus

from fastapi import FastAPI

from fastapi_duno.schemas import Message, Time

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def get_hello():
    return {
        'message': 'hello world!',
    }


@app.get('/time', status_code=HTTPStatus.OK, response_model=Time)
def get_current_time():
    return {
        'time': datetime.datetime.now(),
    }
