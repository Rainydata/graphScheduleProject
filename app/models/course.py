from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "course"
    
    course_ID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    system_room = Column(Boolean, default=False)
    weekly_hours = Column(Integer)

    Teacher_ID = Column(Integer, ForeignKey('teacher.Teacher_ID'))
    Classroom_ID = Column(Integer, ForeignKey('classroom.Classroom_ID'))

    teacher = relationship("Teacher", back_populates="courses")
    classroom = relationship("Classroom", back_populates="courses")
    schedules = relationship("Schedule", back_populates="course")