from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    Name: str
    Weekly_hours: int
    Teacher_ID: int
    Classroom_ID: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    Course_ID: int
    teacher: Optional[int] = None
    classroom: Optional[int] = None

    class Config:
        orm_mode = True
