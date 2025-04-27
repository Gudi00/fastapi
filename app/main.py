import random
import time

import psycopg2
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    data: str

conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                        password='qwerty', cursor_factory=RealDictCursor)
cursor = conn.cursor()
print("Databse was connected")

@app.get("/")
def root():
    return {"message": "/"}

@app.get("/posts")
def get_post():
    cursor.execute("""select * from posts""")
    my_posts = cursor.fetchall()
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""select * from posts where id = %s""", (str(id)))
    my_posts = cursor.fetchone()
    if my_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found {id}")
    return {"data": my_posts}

@app.put("/posts/{id}")
def update_post(id: int, post: Post, response: Response):
    cursor.execute("""update posts set name = %s, price = %s where id = %s returning *""", (post.title, post.data, str(id)))
    my_posts = cursor.fetchone()
    conn.commit()
    if my_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found {id}")
    return {"data": my_posts}

@app.delete("/posts/{id}")
def delete_post(id: int, response: Response):
    cursor.execute("""delete from posts where id = %s returning *""", (str(id)))
    my_posts = cursor.fetchone()
    conn.commit()
    if my_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found {id}")
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create(new_post: Post):
    cursor.execute("""insert into posts values (%s, %s) returning *""", (new_post.title, new_post.data))
    my_posts = cursor.fetchone()
    conn.commit()
    return {"message": my_posts}

