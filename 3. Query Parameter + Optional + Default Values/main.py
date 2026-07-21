from fastapi import FastAPI

app = FastAPI()

# /users?name=vaidik
# /products?price=1000

@app.get("/users")
def get_user(name: str = None):
    return {"Name": name}

@app.get("/products")
def get_products(limit: int = 10):
    return {"Limit": limit}

# Multiple Query Parameters

@app.get("/items")
def get_item(name: str=None, price: int=0):
    return {
        "name": name,
        "price": price
    }