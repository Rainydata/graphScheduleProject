from pydantic import BaseModel

class ScheduleBase(BaseModel):
    Course_ID: int
    day: str
    start_time: str
    end_time: str

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    schedule_ID: int

    class Config:
        orm_mode = True
