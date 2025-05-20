from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Teacher(Base):
    __tablename__ = 'teacher'
    
    Teacher_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)

    courses = relationship("Course", back_populates="teacher")
    availabilities = relationship("TeacherAvailability", back_populates="teacher")