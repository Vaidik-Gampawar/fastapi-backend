# pip install  python-jose 

# from fastapi import FastAPI, Depends, HTTPException, Header
# from jose import jwt
# from datetime import datetime, timedelta, timezone

# app = FastAPI()

# SECRET_KEY = "mysecert"

# ALGORITHM = "HS256"

# # Create Token
# def create_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(minutes=30)
#     to_encode.update({
#         "exp": expire
#     })
#     token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

#     return token


# # Login API(Token generate)
# @app.post("/login")
# def login(username:str, password:str):
#     if username != "admin" or password != "1234":
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid Username and Password"
#         )
#     token = create_token({
#         "sub": username
#     })
#     return {
#         "access_token": token
#     }

# # Token Verify Token
# def verify_token(token: str = Header(None)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid or Expired Token"
#         )

# #Protected Route
# @app.get("/secure")
# def secure_data(user = Depends(verify_token)):
#     return {
#         "message": "Secure Data Accessed",
#         "user": user
#     }


from fastapi import FastAPI, Depends, HTTPException, Header
from jose import jwt
from datetime import datetime, timedelta, timezone

app = FastAPI()
SECERT_KEY = "mysecert"
ALGORITHM = "HS256"

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp": expire
    })
    token = jwt.encode(to_encode, SECERT_KEY, ALGORITHM)

    return token

@app.post("/login")
def login(username: str, password: str):
    if username != "admin" and password != "1234":
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or Password"
        )
    token = create_token({
        "sub": "admin"
    })

    return token

def verify_token(token = Header(None)):
    try:
        payload = jwt.decode(token, SECERT_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )

@app.get("/secure")
def secure_route(user = Depends(verify_token)):
    return {
        "message": "Secure Data Accessed",
        "user": user
    }
