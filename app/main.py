import random

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str = "something"
    data: str

my_posts = [{"title": "first title", "content": "some content", "id": 1}]

@app.get("/")
def root():
    return {"message": "/"}

@app.get("/posts")
def get_post():
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    if id > 5:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found {id}")
    return {"data": id}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create(new_post: Post):
    post_dict = new_post.dict()
    post_dict["id"] = random.randint(0, 1000000)
    my_posts.append(post_dict)

    return {"message": post_dict}