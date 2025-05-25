from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    UserId = Column(Integer, primary_key=True, autoincrement=True)
    RoleCode = Column(String(50))
    Account = Column(String(100), nullable=False)
    Password = Column(String(100), nullable=False)
    UserName = Column(String(100))
    Sex = Column(String(10))
    Email = Column(String(100))
    Phone = Column(String(20))
    IsDelete = Column(Boolean, default=False)

class UserBrief:
    def __init__(self, UserName, Sex):
        self.UserName = UserName
        self.Sex = Sex