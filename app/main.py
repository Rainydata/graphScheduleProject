# main.py
from fastapi import FastAPI
from database import Base, engine
from models import *  # importa todos los modelos para que Base los registre
from routers import teacher, classroom, course, schedule

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir routers
app.include_router(teacher.router, prefix="/teachers", tags=["Teachers"])
app.include_router(classroom.router, prefix="/classrooms", tags=["Classrooms"])
app.include_router(course.router, prefix="/courses", tags=["Courses"])
app.include_router(schedule.router, prefix="/schedules", tags=["Schedules"])
