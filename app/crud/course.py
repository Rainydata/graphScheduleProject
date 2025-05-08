from sqlalchemy.orm import Session
from .. import models, schemas

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(
        Name=course.Name,
        Weekly_hours=course.Weekly_hours,
        Teacher_ID=course.Teacher_ID,
        Classroom_ID=course.Classroom_ID
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.Course_ID == course_id).first()
