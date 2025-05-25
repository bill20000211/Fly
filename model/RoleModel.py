from sqlalchemy import Column, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = 'Role'
    RoleId = Column(UNIQUEIDENTIFIER, primary_key=True, nullable=False)
    RoleName = Column(String(50), nullable=False)
    RoleCode = Column(String(50), nullable=False)
    RoleScope = Column(String(255))
    RolePermission = Column(String)
