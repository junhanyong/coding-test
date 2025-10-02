from sqlalchemy import create_engine, Integer, String, Boolean, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List

# Create connection to SQLite DB
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define DB model
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(Boolean, default=False)

# Create tables in DB based on defined model
Base.metadata.create_all(bind=engine)

def get_db():
    # Create new DB session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI CRUD operations 
app = FastAPI()

# Data validation
class TodoCreate(BaseModel):
    title: str

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True

@app.post("/todo/", response_model=TodoResponse) 
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todo/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(todo_id == Todo.id).first()
    # Check if id exists
    if not todo:
        raise HTTPException(status_code=404, detail="ID does not exist")
    return todo

@app.get("/todo/", response_model=List[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos

