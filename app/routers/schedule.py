from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.schedule_validador import build_schedule_graph_from_db, detect_conflicts

import models
import schemas

router = APIRouter()

@router.get("/validate-schedule/{teacher_id}")
def validate_teacher_schedule(teacher_id: int, db: Session = Depends(get_db)):
    graph, errors = build_schedule_graph_from_db(db, teacher_id)
    if errors:
        raise HTTPException(status_code=404, detail=errors)

    conflicts = detect_conflicts(graph)

    return {
        "teacher_id": teacher_id,
        "conflicts": conflicts,
        "message": "Conflictos detectados" if conflicts else "Horario válido"
    }
