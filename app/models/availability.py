from app.database import Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class TeacherAvailability(Base):
    __tablename__ = 'teacher_availability'
    Teacher_ID = Column(Integer, ForeignKey('teacher.Teacher_ID'), primary_key=True)
    Blocked_Schedules = Column(Integer, ForeignKey('blocked_schedule.Block_ID'), primary_key=True)
    Available = Column(Boolean, default=True)

    teacher = relationship("Teacher", back_populates="availabilities")
    blocked_schedule = relationship("BlockedSchedule", back_populates="teacher_availabilities")

class ClassroomAvailability(Base):
    __tablename__ = 'classroom_availability'
    Classroom_ID = Column(Integer, ForeignKey('classroom.Classroom_ID'), primary_key=True)
    Blocked_Schedules = Column(Integer, ForeignKey('blocked_schedule.Block_ID'), primary_key=True)
    Available = Column(Boolean, default=True)

    classroom = relationship("Classroom", back_populates="availabilities")
    blocked_schedule = relationship("BlockedSchedule", back_populates="classroom_availabilities")