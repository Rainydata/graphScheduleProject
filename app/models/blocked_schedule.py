from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Blocked_Schedule(Base):
    __tablename__ = "blocked_schedules"

    Block_ID = Column(Integer, primary_key=True, index=True)
    Day = Column(String, nullable=False)
    Start_time = Column(Time, nullable=False)
    finish_time = Column(Time, nullable=False)
    type_block = Column(String)

    schedules = relationship("Schedule", back_populates="blocked_schedule")
    teacher_availabilities = relationship("TeacherAvailability", back_populates="blocked_schedule")
    classroom_availabilities = relationship("ClassroomAvailability", back_populates="blocked_schedule")