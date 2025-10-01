from sqlalchemy import create_engine, Integer, String, Boolean, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from fastapi import FastAPI, Depends
from pydantic import BaseModel

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

# id, completed automatically generated
@app.post("/todo/", response_model=TodoResponse) 
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

