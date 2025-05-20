from pydantic import BaseModel

class ClassroomBase(BaseModel):
    Code_Classroom: str
    Name_Classroom: str
    System_room: bool = False

class ClassroomCreate(ClassroomBase):
    pass

class Classroom(ClassroomBase):
    Classroom_ID: int

    class Config:
        orm_mode = True