from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Teacher(Base):
    
    __tablename__ = 'teacher'
    
    Teacher_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)

    courses = relationship("Course", back_populates="teacher")
    schedules = relationship("Schedule", back_populates="teacher")
    availabilities = relationship("TeacherAvailability", back_populates="teacher")