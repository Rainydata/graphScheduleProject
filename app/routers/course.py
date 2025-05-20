from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.course import Course as CourseModel
from app.models.teacher import Teacher
from app.models.classroom import Classroom
from app.schemas.course import CourseCreate, Course
from app.database import get_db

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.course import Course as CourseModel
from app.models.teacher import Teacher
from app.models.classroom import Classroom
from app.schemas.course import CourseCreate, Course
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.Teacher_ID == course.Teacher_ID).first()
    if not teacher:
        raise HTTPException(status_code=400, detail="El docente no existe")

    classroom = db.query(Classroom).filter(Classroom.Classroom_ID == course.Classroom_ID).first()
    if not classroom:
        raise HTTPException(status_code=400, detail="El aula no existe")


    db_course = CourseModel(
        code_academic_space=course.code_academic_space,
        name=course.name,
        franja=course.franja,
        grupo=course.grupo,
        weekly_hours=course.weekly_hours,
        Teacher_ID=course.Teacher_ID,
        Classroom_ID=course.Classroom_ID,
        system_room=course.system_room,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/", response_model=list[Course])
def list_courses(db: Session = Depends(get_db)):
    return db.query(CourseModel).all()



