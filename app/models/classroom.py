from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

class Classroom(Base):
    __tablename__ = "classroom"

    Classroom_ID = Column(Integer, primary_key=True)
    Code_Classroom = Column(String, nullable=False)
    Name_Classroom = Column(String, nullable=False)
    System_room = Column(Boolean, default=False)

    courses = relationship("Course", back_populates="classroom")
    availabilities = relationship("ClassroomAvailability", back_populates="classroom")