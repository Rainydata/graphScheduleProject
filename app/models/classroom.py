from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Classroom(Base):
    __tablename__ = 'classroom'

    Classroom_ID = Column(Integer, primary_key=True, index=True)
    Code_Classroom = Column(String, nullable=False)
    Name_Classroom = Column(String, nullable=False)
    System_room = Column(Boolean, default=False)

    courses = relationship("Course", back_populates="classroom")
    schedules = relationship("Schedule", back_populates="classroom")
    availabilities = relationship("ClassroomAvailability", back_populates="classroom")