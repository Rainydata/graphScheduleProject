from pydantic import BaseModel

class CourseBase(BaseModel):
    code_academic_space: int
    name: str
    franja: str
    grupo: str
    weekly_hours: int
    Teacher_ID: int
    Classroom_ID: int
    system_room: bool = False

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    course_ID: int  # Debe coincidir con el modelo SQLAlchemy

    class Config:
        orm_mode = True