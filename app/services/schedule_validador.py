import networkx as nx
from sqlalchemy.orm import Session
from models import Teacher, Schedule, Course, BlockedSchedule, TeacherAvailability

TIME_BLOCKS = {
    "morning": ["7am-9am", "9am-11am"],
    "afternoon": ["2pm-4pm", "4pm-6pm"],
    "night": ["6pm-8pm", "8pm-10pm"]
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
        course_node = f"{teacher.Name}-{course.Name}"
        G.add_node(course_node, type="course", system_room=course.System_room)

        hours = course.Weekly_hours
        blocks_needed = 2 if hours == 4 else 1
        added_blocks = 0

        for period, blocks in TIME_BLOCKS.items():
            if period not in available_periods:
                continue
            for block in blocks:
                if block == LUNCH_BLOCK:
                    continue
                block_node = f"{period}-{block}"
                if block_node in blocked_times:
                    continue

                G.add_node(block_node, type="time_block")
                G.add_edge(course_node, block_node)
                added_blocks += 1
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
