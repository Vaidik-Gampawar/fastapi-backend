from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name:str
    age:int

app = FastAPI()

@app.post("/create-user")
def create_user(data:User):
    return {
        "message": "User Created",
        "data": data
    }