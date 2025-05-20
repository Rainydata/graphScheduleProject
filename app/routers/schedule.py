from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.schedule_validador import build_teacher_schedule_and_conflicts
from app.models.schedule import Schedule as ScheduleModel
from app.models.course import Course
from app.models.teacher import Teacher
from app.models.availability import TeacherAvailability
from app.schemas.schedule import ScheduleCreate, Schedule
from fastapi import status

router = APIRouter()
@router.get("/validate-schedule/{teacher_id}")
def validate_teacher_schedule(teacher_id: int, db: Session = Depends(get_db)):
    from app.services.schedule_validador import build_teacher_schedule_and_conflicts
    return build_teacher_schedule_and_conflicts(db, teacher_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    # Obtener el curso correspondiente
    course = db.query(Course).filter(Course.course_ID == schedule.Course_ID).first()
    if not course:
        raise HTTPException(status_code=400, detail="El curso no existe")

    # Validar si la materia requiere sala de sistemas
    classroom = db.query(Course).filter(Course.Classroom_ID == course.Classroom_ID).first()
    if course.system_room and not classroom.classroom.System_room:
        raise HTTPException(
            status_code=400,
            detail="La materia requiere sala de sistemas, pero el aula seleccionada no es de sistemas."
        )

    # Validar bloques de 4h y 3h semanales (NO insertar si viola la regla)
    existing_schedules = db.query(ScheduleModel).filter(ScheduleModel.Course_ID == schedule.Course_ID).all()
    if course.weekly_hours == 4:
        if len(existing_schedules) >= 2:
            raise HTTPException(status_code=400, detail="Un curso de 4h solo puede tener 2 bloques de 2h.")
        dias = set([s.day for s in existing_schedules])
        if schedule.day in dias:
            raise HTTPException(status_code=400, detail="Los bloques de un curso de 4h deben estar en días diferentes.")
    if course.weekly_hours == 3:
        if len(existing_schedules) >= 1:
            raise HTTPException(status_code=400, detail="Un curso de 3h solo puede tener 1 bloque de 3h.")

    # Validar bloqueos del profesor (NO insertar si está bloqueado)
    from app.models.availability import TeacherAvailability
    teacher_blocks = db.query(TeacherAvailability).filter(
        TeacherAvailability.Teacher_ID == course.Teacher_ID,
        TeacherAvailability.Available == False
    ).all()
    for tb in teacher_blocks:
        block = tb.blocked_schedule
        if (block.Day == schedule.day and
            block.Start_time.strftime("%H:%M") == schedule.start_time and
            block.Finish_time.strftime("%H:%M") == schedule.end_time):
            raise HTTPException(status_code=400, detail="El profesor tiene bloqueado ese horario.")

    # Validar conflicto de salón (NO puede haber dos grupos en el mismo salón, mismo horario)
    overlapping_salon = db.query(ScheduleModel).join(Course).filter(
        ScheduleModel.day == schedule.day,
        ScheduleModel.start_time == schedule.start_time,
        ScheduleModel.end_time == schedule.end_time,
        Course.Classroom_ID == course.Classroom_ID,
        Course.grupo != course.grupo  # Solo conflicto si es otro grupo
    ).first()
    if overlapping_salon:
        raise HTTPException(
            status_code=400,
            detail="Conflicto de salón: ya hay otro grupo en ese salón y horario."
        )

    # Validar conflicto de profesor (NO puede haber dos grupos con el mismo profe en el mismo horario)
    overlapping_prof = db.query(ScheduleModel).join(Course).filter(
        ScheduleModel.day == schedule.day,
        ScheduleModel.start_time == schedule.start_time,
        ScheduleModel.end_time == schedule.end_time,
        Course.Teacher_ID == course.Teacher_ID,
        Course.grupo != course.grupo  # Solo conflicto si es otro grupo
    ).first()
    if overlapping_prof:
        raise HTTPException(
            status_code=400,
            detail="Conflicto de profesor: el profesor ya tiene otro grupo en ese horario."
        )

    # Guardar el horario si todo está bien
    db_schedule = ScheduleModel(
        Course_ID=schedule.Course_ID,
        day=schedule.day,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return {
        "schedule_ID": db_schedule.schedule_ID,
        "Course_ID": db_schedule.Course_ID,
        "day": db_schedule.day,
        "start_time": db_schedule.start_time,
        "end_time": db_schedule.end_time,
        "message": "Horario asignado correctamente"
    }


@router.get("/graph-data/")
def get_all_schedules_with_conflicts(db: Session = Depends(get_db)):
    from app.models.schedule import Schedule as ScheduleModel
    schedules = db.query(ScheduleModel).all()
    block_salon = {}
    block_prof = {}
    for sched in schedules:
        course = sched.course
        classroom = course.classroom
        key_salon = (sched.day, sched.start_time, classroom.Classroom_ID)
        key_prof = (sched.day, sched.start_time, course.Teacher_ID)
        block_salon.setdefault(key_salon, []).append(sched)
        block_prof.setdefault(key_prof, []).append(sched)
    result = []
    for sched in schedules:
        course = sched.course
        teacher = course.teacher
        classroom = course.classroom
        key_salon = (sched.day, sched.start_time, classroom.Classroom_ID)
        key_prof = (sched.day, sched.start_time, course.Teacher_ID)
        conflicto = ""
        if len(block_salon[key_salon]) > 1:
            conflicto += "aula"
        if len(block_prof[key_prof]) > 1:
            if conflicto:
                conflicto += ",profesor"
            else:
                conflicto = "profesor"
        result.append({
            "day": sched.day,
            "block": f"{sched.start_time}-{sched.end_time}",
            "materia": course.name,
            "profesor": teacher.Name,
            "aula": classroom.Name_Classroom,
            "conflicto": conflicto
        })
    return result

# funcion que permite mostra la primera en conflicto en el calendario raiz

#@router.get("/all/")
#def get_all_schedules(db: Session = Depends(get_db)):
    #from app.models.schedule import Schedule as ScheduleModel
   # schedules = db.query(ScheduleModel).all()
    
    # Agrupar por bloque (día + hora + salón/profesor)
    #block_salon = {}  # (day, time, classroom_id) -> [schedules]
    #block_prof = {}   # (day, time, teacher_id) -> [schedules]
    
    #for sched in schedules:
     #   course = sched.course
     #   classroom = course.classroom
     #   key_salon = (sched.day, sched.start_time, classroom.Classroom_ID)
     #   key_prof = (sched.day, sched.start_time, course.Teacher_ID)
        
        # Usar setdefault para simplificar
    #    block_salon.setdefault(key_salon, []).append(sched)
    #    block_prof.setdefault(key_prof, []).append(sched)

    #result = []
    # Solo incluir horarios "sanos" (primeros en cada bloque)
    #for sched in schedules:
     #   course = sched.course
      #  classroom = course.classroom
      #  key_salon = (sched.day, sched.start_time, classroom.Classroom_ID)
      #  key_prof = (sched.day, sched.start_time, course.Teacher_ID)
        
        # Solo incluir si es el primer horario en ambos bloques
      #  if (sched == block_salon[key_salon][0] and 
      #      sched == block_prof[key_prof][0]):
      #      result.append({
      #          "day": sched.day,
      #          "block": f"{sched.start_time}-{sched.end_time}",
      #          "materia": course.name,
     #           "profesor": course.teacher.Name,
     #           "aula": classroom.Name_Classroom
    #        })
    
   # return result

@router.get("/all/")
def get_all_schedules(db: Session = Depends(get_db)):
    from app.models.schedule import Schedule as ScheduleModel
    schedules = db.query(ScheduleModel).all()
    
    # Agrupar por bloque (día + hora + salón/profesor)
    block_salon = {}  # (day, time, classroom_id) -> [schedules]
    block_prof = {}   # (day, time, teacher_id) -> [schedules]
    
    for sched in schedules:
        course = sched.course
        classroom = course.classroom
        key_salon = (sched.day, sched.start_time, classroom.Classroom_ID)
        key_prof = (sched.day, sched.start_time, course.Teacher_ID)
        
        block_salon.setdefault(key_salon, []).append(sched)
        block_prof.setdefault(key_prof, []).append(sched)

    result = []
    # Solo incluir horarios si NO hay NINGÚN conflicto en ese bloque
    for sched in schedules:
        course = sched.course
        classroom = course.classroom
        key_salon = (sched.day, sched.start_time, classroom.Classroom_ID)
        key_prof = (sched.day, sched.start_time, course.Teacher_ID)
        
        # Verificar que NO haya conflictos (solo un horario por bloque)
        if (len(block_salon[key_salon]) == 1 and 
            len(block_prof[key_prof]) == 1):
            result.append({
                "day": sched.day,
                "block": f"{sched.start_time}-{sched.end_time}",
                "materia": course.name,
                "profesor": course.teacher.Name,
                "aula": classroom.Name_Classroom
            })
    
    return result

