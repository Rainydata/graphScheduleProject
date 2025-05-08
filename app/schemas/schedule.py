from pydantic import BaseModel
from typing import Optional

class ScheduleBase(BaseModel):
    Course_ID: int
    Teacher_ID: int
    Classroom_ID: int
    Schedule_Type: str
    IsMainBlocked: Optional[bool] = False

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    Schedule_ID: int

    class Config:
        orm_mode = True
