from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import FastAPI, Depends

app = FastAPI()

#Database connection URL
DATABASE_URL = "sqlite:///./test.db"

# Engine (Connects SQLAlchemy to the database)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session Factory (Creates database sessions)
sessionLocal = sessionmaker(bind=engine)

# Base class for all database models
Base = declarative_base()

# Database table model
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Dependency (Provides a database session to every API request)
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos")
def create_todo(title: str, db: Session = Depends(get_db)):
    todo = Todo(title=title, completed="False")
    db.add(todo)
    db.commit()
    db.refresh(todo)

    return {
        "message": "Todo Created",
        "data": todo
    }