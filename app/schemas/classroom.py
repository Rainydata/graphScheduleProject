from pydantic import BaseModel
from typing import List, Optional
import schemas

class ClassroomBase(BaseModel):
    Code_Classroom: str
    Name_Classroom: str
    System_room: Optional[bool] = False

class ClassroomCreate(ClassroomBase):
    pass

class Classroom(ClassroomBase):
    Classroom_ID: int
    courses: List[int] = []

    class Config:
        orm_mode = True
