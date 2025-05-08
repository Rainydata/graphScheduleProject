from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/classrooms/", response_model=schemas.Classroom)
def create_classroom(classroom: schemas.ClassroomCreate, db: Session = Depends(get_db)):
    return crud.create_classroom(db=db, classroom=classroom)

@router.get("/classrooms/{classroom_id}", response_model=schemas.Classroom)
def get_classroom(classroom_id: int, db: Session = Depends(get_db)):
    return crud.get_classroom(db=db, classroom_id=classroom_id)
