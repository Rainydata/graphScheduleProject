import networkx as nx
from sqlalchemy.orm import Session
from app.models import Teacher, Schedule, Course, BlockedSchedule, TeacherAvailability

TIME_BLOCKS = {
    "morning": ["7am-9am", "9am-11am", "7am-10am"],
    "afternoon": ["2pm-4pm", "4pm-6pm", "2pm-5pm"],
    "night": ["6pm-8pm", "8pm-10pm", "6pm-9pm"]
}
LUNCH_BLOCK = "1pm-2pm"

def build_schedule_graph_from_db(db: Session, teacher_id: int):
    G = nx.Graph()

    teacher: Teacher = db.query(Teacher).filter(Teacher.Teacher_ID == teacher_id).first()
    if not teacher:
        return None, ["Profesor no encontrado"]

    # Disponibilidad del profesor
    available_periods = {"morning", "afternoon", "night"}
    blocked_times = set()

    # Obtener bloques no disponibles
    for availability in teacher.availabilities:
        block = availability.blocked_schedule
        if not availability.Available:
            blocked_times.add(f"{block.Day}-{block.Start_time.strftime('%I%p')}-{block.Finish_time.strftime('%I%p')}")

    for course in teacher.courses:
        course_node = f"{teacher.Name}-{course.name}"
        G.add_node(course_node, type="course", system_room=course.system_room)

        hours = course.weekly_hours
        if hours == 4:
            blocks_needed = 2
            valid_blocks = ["7am-9am", "9am-11am", "2pm-4pm", "4pm-6pm", "6pm-8pm", "8pm-10pm"]
        elif hours == 3:
            blocks_needed = 1
            valid_blocks = ["7am-10am", "2pm-5pm", "6pm-9pm"]
        else:
            blocks_needed = 1
            valid_blocks = ["7am-9am", "9am-11am", "2pm-4pm", "4pm-6pm", "6pm-8pm", "8pm-10pm"]

        added_blocks = 0
        used_days = set()
        for period, blocks in TIME_BLOCKS.items():
            if period not in available_periods:
                continue
            for block in blocks:
                if block == LUNCH_BLOCK or block not in valid_blocks:
                    continue
                block_node = f"{period}-{block}"
                # Aquí deberías obtener el día real si lo tienes, por ahora se omite
                # day = ...
                # if hours == 4 and day in used_days:
                #     continue  # No permitir dos bloques el mismo día para 4h
                if block_node in blocked_times:
                    continue

                G.add_node(block_node, type="time_block")
                G.add_edge(course_node, block_node)
                added_blocks += 1
                # if hours == 4:
                #     used_days.add(day)
                if added_blocks >= blocks_needed:
                    break
            if added_blocks >= blocks_needed:
                break

    return G, []

def detect_conflicts(graph: nx.Graph):
    conflicts = []
    for node in graph.nodes:
        if graph.nodes[node]['type'] == 'time_block':
            neighbors = list(graph.neighbors(node))
            if len(neighbors) > 1:
                conflicts.append(f"Conflicto en {node}: {', '.join(neighbors)}")
    return conflicts

#funcion que no pinta la primera en conflicto

'''
def build_teacher_schedule_and_conflicts(db: Session, teacher_id: int):
    from app.models import Schedule, Course, Classroom, Teacher

    # Obtener TODOS los horarios del sistema
    all_schedules = db.query(Schedule).all()
    
    # Agrupar horarios por bloque (día + hora + salón/profesor)
    block_salon = {}  # (day, time, classroom_id) -> [schedules]
    block_prof = {}   # (day, time, teacher_id) -> [schedules]
    
    for sched in all_schedules:
        # Agrupa por salón
        key_salon = (sched.day, sched.start_time, sched.course.Classroom_ID)
        if key_salon not in block_salon:
            block_salon[key_salon] = []
        block_salon[key_salon].append(sched)
        
        # Agrupa por profesor
        key_prof = (sched.day, sched.start_time, sched.course.Teacher_ID)
        if key_prof not in block_prof:
            block_prof[key_prof] = []
        block_prof[key_prof].append(sched)

    # Filtra los horarios del profesor seleccionado
    teacher_schedules = [s for s in all_schedules if s.course.Teacher_ID == teacher_id]
    
    schedule_list = []
    conflicts = []

    for sched in teacher_schedules:
        course = sched.course
        classroom = course.classroom
        conflicto = ""

        # Verifica si este horario NO es el primero en su bloque
        key_salon = (sched.day, sched.start_time, course.Classroom_ID)
        key_prof = (sched.day, sched.start_time, course.Teacher_ID)
        
        # Solo marca conflicto si NO es el primer horario en ese bloque
        if len(block_salon[key_salon]) > 1 and sched != block_salon[key_salon][0]:
            conflicto = "Conflicto: mismo salón"
            conflicts.append(f"Conflicto en {sched.day} {sched.start_time}: {course.name}")
            
        if len(block_prof[key_prof]) > 1 and sched != block_prof[key_prof][0]:
            if conflicto:
                conflicto += " y profesor"
            else:
                conflicto = "Conflicto: mismo profesor"
            conflicts.append(f"Conflicto en {sched.day} {sched.start_time}: {course.name}")

        schedule_list.append({
            "day": sched.day,
            "block": f"{sched.start_time}-{sched.end_time}",
            "materia": course.name,
            "salon": classroom.Name_Classroom,
            "profesor": course.teacher.Name,
            "conflicto": conflicto
        })

    return {
        "schedule": schedule_list,
        "conflicts": list(set(conflicts)),
        "message": "Conflictos detectados" if conflicts else "Horario válido"
    }
'''

def build_teacher_schedule_and_conflicts(db: Session, teacher_id: int):
    from app.models import Schedule, Course, Classroom, Teacher

    # Obtener TODOS los horarios del sistema
    all_schedules = db.query(Schedule).all()
    
    # Agrupar horarios por bloque (día + hora + salón/profesor)
    block_salon = {}  # (day, time, classroom_id) -> [schedules]
    block_prof = {}   # (day, time, teacher_id) -> [schedules]
    
    for sched in all_schedules:
        # Agrupa por salón
        key_salon = (sched.day, sched.start_time, sched.course.Classroom_ID)
        if key_salon not in block_salon:
            block_salon[key_salon] = []
        block_salon[key_salon].append(sched)
        
        # Agrupa por profesor
        key_prof = (sched.day, sched.start_time, sched.course.Teacher_ID)
        if key_prof not in block_prof:
            block_prof[key_prof] = []
        block_prof[key_prof].append(sched)

    # Filtra los horarios del profesor seleccionado
    teacher_schedules = [s for s in all_schedules if s.course.Teacher_ID == teacher_id]
    
    schedule_list = []
    conflicts = []

    for sched in teacher_schedules:
        course = sched.course
        classroom = course.classroom
        conflicto = ""

        key_salon = (sched.day, sched.start_time, course.Classroom_ID)
        key_prof = (sched.day, sched.start_time, course.Teacher_ID)
        
        # Marca conflicto si hay más de un horario en el bloque (todos en conflicto)
        if len(block_salon[key_salon]) > 1:
            conflicto = "Conflicto: mismo salón"
            conflicts.append(f"Conflicto en {sched.day} {sched.start_time}: {course.name}")
            
        if len(block_prof[key_prof]) > 1:
            if conflicto:
                conflicto += " y profesor"
            else:
                conflicto = "Conflicto: mismo profesor"
            conflicts.append(f"Conflicto en {sched.day} {sched.start_time}: {course.name}")

        schedule_list.append({
            "day": sched.day,
            "block": f"{sched.start_time}-{sched.end_time}",
            "materia": course.name,
            "salon": classroom.Name_Classroom,
            "profesor": course.teacher.Name,
            "conflicto": conflicto
        })

    return {
        "schedule": schedule_list,
        "conflicts": list(set(conflicts)),
        "message": "Conflictos detectados" if conflicts else "Horario válido"
    }