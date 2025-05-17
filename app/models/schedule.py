from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Schedule(Base):
    __tablename__ = 'schedule'

    Schedule_ID = Column(Integer, primary_key=True, index=True)
    Course_ID = Column(Integer, ForeignKey('course.course_ID'))
    Teacher_ID = Column(Integer, ForeignKey('teacher.Teacher_ID'))
    Classroom_ID = Column(Integer, ForeignKey('classroom.Classroom_ID'))
    Blocked_Schedules = Column(Integer, ForeignKey('blocked_schedule.Block_ID'))
    Schedule_Type = Column(String)
    IsMainBlocked = Column(Boolean, default=False)

    course = relationship("Course", back_populates="schedules")
    teacher = relationship("Teacher", back_populates="schedules")
    classroom = relationship("Classroom", back_populates="schedules")
    blocked_schedule = relationship("BlockedSchedule", back_populates="schedules")