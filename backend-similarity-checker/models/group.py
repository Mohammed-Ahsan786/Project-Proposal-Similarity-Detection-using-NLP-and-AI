from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key = True, autoincrement = True)
    group_name = Column(String(100), unique = True, nullable = False)
    leader_id = Column(Integer, ForeignKey('students.student_id'), nullable = False)
    leader = relationship('Student', back_populates = 'groups')
    projects = relationship('Project', back_populates = 'group')
