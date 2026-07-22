from fastapi import FastAPI,Request
import time

app = FastAPI()

# @app.middleware("http")
# async def my_middleware(request: Request, call_next):
#     print("Request Sent")

#     response = await call_next(request)

#     print("Response Sent")

#     return response

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    complete_time = time.time() - start_time
    
    print(f"Path: {request.url.path} | Time: {complete_time}")
    
    return response

