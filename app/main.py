from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import teacher, classroom, course, schedule
from app.database import Base, engine
from app.models import Teacher, Classroom, Course, Schedule, TeacherAvailability, ClassroomAvailability, BlockedSchedule

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(teacher.router, prefix="/teachers", tags=["Teachers"])
app.include_router(classroom.router, prefix="/classrooms", tags=["Classrooms"])
app.include_router(course.router, prefix="/courses", tags=["Courses"])
app.include_router(schedule.router, prefix="/schedules", tags=["Schedules"])

@app.get("/")
def read_root():
    return {"message": "¡API de horarios funcionando!"}