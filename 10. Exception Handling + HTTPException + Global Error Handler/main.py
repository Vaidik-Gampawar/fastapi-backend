from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()


class UserNotFoundException(Exception):
    def __init__(self, name:str):
        self.name = name

@app.exception_handler(UserNotFoundException)
def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": "User not found" 
        }
    )

@app.get("/users/{user_name}")
def get_user(user_name:str):
    if user_name != "vaidik":
        raise UserNotFoundException(user_name)
    return {
        "name": user_name
    }

# @app.get("/users/{user_id}")
# def get_user(user_id:int):
#     if user_id != 1:
#         raise HTTPException(
#             status_code=404,
#             detail="User not Found"
#         )
#     return {
#         "message": "User Found",
#         "data": {
#             "id": 1,
#             "name": "vaidik"
#         }
#     }