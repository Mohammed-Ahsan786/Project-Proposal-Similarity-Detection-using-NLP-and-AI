from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
class Project(Base):
    __tablename__ = 'projects'
    project_id  = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String(255), nullable = False)
    abstract = Column(Text, nullable = False)
    category = Column(String(300), nullable = False)
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable = False)
    status = Column(String(50), default = 'pending', nullable = False)
    group = relationship('Group', back_populates='projects')