from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(
        name=course.name,
        system_room=course.system_room,
        weekly_hours=course.weekly_hours,
        Teacher_ID=course.Teacher_ID,
        Classroom_ID=course.Classroom_ID
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/", response_model=list[schemas.Course])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()