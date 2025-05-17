from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = models.Teacher(Name=teacher.Name)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/", response_model=list[schemas.Teacher])
def list_teachers(db: Session = Depends(get_db)):
    return db.query(models.Teacher).all()