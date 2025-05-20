from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "course"

    course_ID = Column(Integer, primary_key=True)
    code_academic_space = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    franja = Column(String, nullable=False)
    grupo = Column(String, nullable=False)
    weekly_hours = Column(Integer, nullable=False)
    system_room = Column(Boolean, default=False)
    Teacher_ID = Column(Integer, ForeignKey("teacher.Teacher_ID"))
    Classroom_ID = Column(Integer, ForeignKey("classroom.Classroom_ID"))

    schedules = relationship("Schedule", back_populates="course")
    teacher = relationship("Teacher", back_populates="courses")
    classroom = relationship("Classroom", back_populates="courses")