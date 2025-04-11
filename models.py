from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    app_password = Column(String)
    targets = relationship("TargetUser", back_populates="owner")
    logs = relationship("FollowLog", back_populates="owner")

class TargetUser(Base):
    __tablename__ = "target_users"
    id = Column(Integer, primary_key=True, index=True)
    handle = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="targets")

class FollowLog(Base):
    __tablename__ = "follow_logs"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="logs")
