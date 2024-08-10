from sqlalchemy import Integer, Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base
class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(100), nullable = False)
    roll_no = Column(String(20), nullable = False)
    branch = Column(String(50), nullable = False)
    groups = relationship('Group', back_populates='leader')