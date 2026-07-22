from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user():
    return {
        "message": "User Created"
    }

@app.get("/users")
def get_users():
    return {
        "status": "Success",
        "message": "User Fetched",
        "data": {
            "name": "vaidik",
            "age": 21
        }
    }

@app.get("/users/{user_id}")
def get_user(user_id:int):
    if user_id != 1:
        raise HTTPException (
            status_code=404,
            detail="User not found"
        )
    return {
        "message": "User Found",
        "data": {
            "name": "vaidik",
            "age": 21
        }
    }