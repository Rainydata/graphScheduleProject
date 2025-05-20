from pydantic import BaseModel

class TeacherBase(BaseModel):
    Name: str

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    Teacher_ID: int

    class Config:
        orm_mode = True