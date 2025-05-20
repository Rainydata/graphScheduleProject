from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.classroom import Classroom, ClassroomCreate
from app.models.classroom import Classroom as ClassroomModel
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Classroom)
def create_classroom(classroom: ClassroomCreate, db: Session = Depends(get_db)):
    db_classroom = ClassroomModel(
        Name_Classroom=classroom.Name_Classroom,
        Code_Classroom=classroom.Code_Classroom,
        System_room=classroom.System_room,
    )
    db.add(db_classroom)
    db.commit()
    db.refresh(db_classroom)
    return db_classroom

@router.get("/", response_model=list[Classroom])
def list_classrooms(db: Session = Depends(get_db)):
    return db.query(ClassroomModel).all()