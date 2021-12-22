from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import db_helper
import const
import uvicorn


class Cat(BaseModel):
    id: int = None
    name: str
    about: str
    avatarUrl: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/kitties')
def kitties_list():
    """
    Получение списка кошек.
    """
    sql = """
        select
            id,
            name,
            description as about,
            photo_url as "avatarUrl"
        from cat
        order by name
    """
    return db_helper.execute_query(sql)


@app.post('/kitties/')
def create(payload: Cat):
    """
    Создание карточки кошки.
    """
    sql = """
        insert into cat (name, description, photo_url)
        values (%s::text, %s::text, %s::text)
    """
    db_helper.execute_query(
        sql,
        payload.name,
        payload.about,
        payload.avatarUrl
    )


@app.put('/kitties/{id}')
def update(id: int, payload: Cat):
    """
    Обновление карточки кошки.
    """
    sql = """
        update cat
        set name = %s::text, description = %s::text, photo_url = %s::text
        where id = %s::int
    """
    db_helper.execute_query(
        sql,
        payload.name,
        payload.about,
        payload.avatarUrl,
        payload.id
    )


@app.delete('/kitties/{id}')
def delete(id: int):
    """
    Удаление карточки кошки.
    """
    sql = 'delete from cat where id = %s::int'
    db_helper.execute_query(sql, id)


# Или из консоли: uvicorn main:app --host 0.0.0.0 --port 3000 --debug
if __name__ == '__main__':
    uvicorn.run(app, host=const.APP_IP, port=const.APP_PORT)
