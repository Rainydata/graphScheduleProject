from sqlalchemy.orm import Session
from .. import models, schemas

def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
    db_schedule = models.Schedule(
        Course_ID=schedule.Course_ID,
        Teacher_ID=schedule.Teacher_ID,
        Classroom_ID=schedule.Classroom_ID,
        Schedule_Type=schedule.Schedule_Type,
        IsMainBlocked=schedule.IsMainBlocked
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def get_schedule(db: Session, schedule_id: int):
    return db.query(models.Schedule).filter(models.Schedule.Schedule_ID == schedule_id).first()
