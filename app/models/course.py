from sqlalchemy import column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Course(Base):
    __tablename__ = "course"
    
    course_ID = column(Integer, primary_key=True, )
    