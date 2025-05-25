from sqlalchemy import Column, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NodeAcross(Base):
    __tablename__ = 'NodeAcross'
    ID = Column(UNIQUEIDENTIFIER, primary_key=True, nullable=False)
    NodeId = Column(UNIQUEIDENTIFIER, nullable=False)
    CallNodeId = Column(UNIQUEIDENTIFIER, nullable=False)
    FunctionName = Column(String(100), nullable=False)
