from sqlalchemy.orm import Session
from .. import models, schemas

def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(Name=teacher.Name)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.Teacher_ID == teacher_id).first()
