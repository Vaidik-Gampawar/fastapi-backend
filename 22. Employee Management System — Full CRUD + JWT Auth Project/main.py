from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, Session
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


DATABASE_URL = "sqlite:///./emp_data.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

sessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_emp")
def create_emp(name: str, password: str, db: Session = Depends(get_db)):
    emp = Employee(name=name, password=password)
    db.add(emp)
    db.commit()
    db.refresh(emp)

    return {
        "message": "Employee Created",
        "data": emp
    }



@app.get("/emp_data/{emp_id}")
def get_emp_by_id(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()

    if not emp:
        raise HTTPException(
            status_code=404,
            detail="Employee Not Found"
        )

    return {
        "message": "Employee Data Found",
        "data": emp
    }

@app.put("/update_emp/{emp_id}")
def update_todo(emp_id:int, name:str, password:str, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()

    if not emp:
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )

    emp.name = name
    emp.password = password
    
    db.commit()
    db.refresh(emp)
    
    return {
        "message": "Employee Data Update",
        "data": emp
    }

@app.delete("/delete_emp/{emp_id}")
def delete_todo(emp_id:int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()

    if not emp:
        raise HTTPException(
            status_code=404,
            detail="Employee Data Not Found"
        )
    db.delete(emp)
    db.commit()

    return {
        "message": "Employee Data Deleted",
        "data": emp
    }

# Login API
@app.post("/login/{emp_id}")
def login(emp_id: int, name: str, password: str, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(
            status_code=404,
            detail="Employee Data Not Found"
        )
    if name != emp.name or password != emp.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or Password"
        )

    token = create_token({
        "sub": name
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

# Secure Route
@app.get("/emp_data")
def get_all_emp(user = Depends(verify_token) ,db: Session = Depends(get_db)):
    emp = db.query(Employee).all()

    if not emp:
        raise HTTPException(
            status_code=404,
            detail="No Employee Found"
        )

    return {
        "message": "All Employee Data Retrieved",
        "user": user,
        "data": emp
    }