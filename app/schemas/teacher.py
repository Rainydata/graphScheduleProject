from pydantic import BaseModel
from typing import List, Optional
import schemas

class TeacherBase(BaseModel):
    Name: str

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    Teacher_ID: int
    courses: List[int] = []
    availabilities: List[int] = []

    class Config:
        orm_mode = True
