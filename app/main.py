from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, database
from .database import engine
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="DevOps Project", version="1.0.0", lifespan=lifespan)


class StudentCreate(BaseModel):
    reg_no: str
    name: str
    semester: int
    section: str


class StudentResponse(StudentCreate):
    id: int

    model_config = {"from_attributes": True}


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(database.text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return {
        "status": "ok",
        "db": db_status,
        "student": "2312274",
    }


@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(
        models.Student.reg_no == student.reg_no
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Registration number already exists")
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students", response_model=list[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@app.get("/students/{reg_no}", response_model=StudentResponse)
def get_student(reg_no: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.reg_no == reg_no
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.delete("/students/{reg_no}", status_code=204)
def delete_student(reg_no: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.reg_no == reg_no
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return None
