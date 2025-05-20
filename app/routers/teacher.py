from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.teacher import Teacher as TeacherModel
from app.schemas.teacher import TeacherCreate, Teacher
from app.database import get_db
from app.models.blocked_schedule import BlockedSchedule
from app.models.availability import TeacherAvailability
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class BlockScheduleRequest(BaseModel):
    teacher_id: int
    day: str
    start_time: str
    end_time: str

@router.post("/", response_model=Teacher)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = TeacherModel(Name=teacher.Name)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/", response_model=list[Teacher])
def list_teachers(db: Session = Depends(get_db)):
    return db.query(TeacherModel).all()
def parse_time(tstr):
    # Admite "7am", "09:00", "13:00", "7:00am", etc.
    try:
        return datetime.strptime(tstr.strip(), "%I%p").time()
    except ValueError:
        try:
            return datetime.strptime(tstr.strip(), "%H:%M").time()
        except ValueError:
            return datetime.strptime(tstr.strip(), "%H:%M:%S").time()

@router.post("/block-schedule/")
def block_teacher_schedule(req: BlockScheduleRequest, db: Session = Depends(get_db)):
    teacher_id = req.teacher_id
    day = req.day
    start_time = parse_time(req.start_time)
    end_time = parse_time(req.end_time)

    teacher = db.query(TeacherModel).filter(TeacherModel.Teacher_ID == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    # Busca o crea el bloque
    block = db.query(BlockedSchedule).filter_by(
        Day=day, Start_time=start_time, Finish_time=end_time
    ).first()
    if not block:
        block = BlockedSchedule(Day=day, Start_time=start_time, Finish_time=end_time, type_block="manual")
        db.add(block)
        db.commit()
        db.refresh(block)

    # Relaciona el profesor con el bloque (Available=False)
    existing = db.query(TeacherAvailability).filter_by(
        Teacher_ID=teacher_id, Blocked_Schedules=block.Block_ID
    ).first()
    if existing:
        existing.Available = False
    else:
        availability = TeacherAvailability(
            Teacher_ID=teacher_id,
            Blocked_Schedules=block.Block_ID,
            Available=False
        )
        db.add(availability)
    db.commit()
    return {"message": "Bloqueo registrado correctamente"}

@router.post("/unblock-schedule/")
def unblock_teacher_schedule(req: BlockScheduleRequest, db: Session = Depends(get_db)):
    teacher_id = req.teacher_id
    day = req.day
    start_time = parse_time(req.start_time)
    end_time = parse_time(req.end_time)

    block = db.query(BlockedSchedule).filter_by(
        Day=day, Start_time=start_time, Finish_time=end_time
    ).first()
    if not block:
        raise HTTPException(status_code=404, detail="Bloque no encontrado")

    availability = db.query(TeacherAvailability).filter_by(
        Teacher_ID=teacher_id, Blocked_Schedules=block.Block_ID
    ).first()
    if not availability:
        raise HTTPException(status_code=404, detail="No hay bloqueo para ese horario")
    availability.Available = True
    db.commit()
    return {"message": "Bloqueo eliminado correctamente"}

@router.get("/{teacher_id}/blocked/")
def get_teacher_blocked(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(TeacherModel).filter(TeacherModel.Teacher_ID == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    blocks = []
    for availability in teacher.availabilities:
        if not availability.Available:
            block = availability.blocked_schedule
            blocks.append({
                "day": block.Day,
                "start_time": block.Start_time.strftime("%I%p").lstrip("0").lower(),
                "end_time": block.Finish_time.strftime("%I%p").lstrip("0").lower()
            })
    return blocks