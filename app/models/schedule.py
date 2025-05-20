from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Schedule(Base):
    __tablename__ = "schedule"

    schedule_ID = Column(Integer, primary_key=True)
    Course_ID = Column(Integer, ForeignKey("course.course_ID"))
    day = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)

    course = relationship("Course", back_populates="schedules")