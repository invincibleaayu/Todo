from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal, engine
import models
from models import User, Todo
from schemas import  UserCreate, TodoCreate, TodoUpdate, UserRead, TodoRead

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate,  db: Session = Depends(get_db)):
    try:
        db_user = User(email=user.email, hashed_password="example")
        print(db_user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int):
    try:
        db = SessionLocal()
        db_user = db.query(User).get(user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/todos", response_model=TodoRead)
def create_todo(todo: TodoCreate):
    try:
        db = SessionLocal()
        db_todo = Todo(
            title=todo.title,
            description=todo.description,
            owner_id=todo.owner_id
        )
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/todos/{todo_id}", response_model=TodoRead)
def read_todo(todo_id: int):
    try:
        db = SessionLocal()
        db_todo = db.query(Todo).get(todo_id)
        if db_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return db_todo
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.put("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, todo: TodoUpdate):
    try:
        db = SessionLocal()
        db_todo = db.query(Todo).get(todo_id)
        if db_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        db_todo.title = todo.title
        db_todo.description = todo.description
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    try:
        db = SessionLocal()
        db_todo = db.query(Todo).get(todo_id)
        if db_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        db.delete(db_todo)
        db.commit()
        return {"message": "Todo deleted"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")