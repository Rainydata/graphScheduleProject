# main.py
from fastapi import FastAPI
from database import Base, engine
from models import *  # importa todos los modelos para que Base los registre
from routers import teacher, classroom, course, schedule
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O especifica ["http://localhost:3000"] 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "¡API de horarios funcionando!"}

# Incluir routers
app.include_router(teacher.router, prefix="/teachers", tags=["Teachers"])
app.include_router(classroom.router, prefix="/classrooms", tags=["Classrooms"])
app.include_router(course.router, prefix="/courses", tags=["Courses"])
app.include_router(schedule.router, prefix="/schedules", tags=["Schedules"])
