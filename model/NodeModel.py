from sqlalchemy import Column, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Node(Base):
    __tablename__ = 'Node'
    NodeId = Column(UNIQUEIDENTIFIER, primary_key=True, nullable=False)
    NodeName = Column(String(50), nullable=False)
    NodeGroup = Column(String(50))
    NodeArea = Column(String(50))
    Parm = Column(String)
    Icon = Column(String(100))
    NodeIndex = Column(String(100))
