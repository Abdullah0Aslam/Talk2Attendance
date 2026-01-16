from sqlalchemy import Column, Integer, String, DateTime, Date, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    department = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    start_date = Column(Date, nullable=False)
    resign_date = Column(Date, nullable=True)
    total_duration = Column(Integer, nullable=True)
    
    attendances = relationship("Attendance", back_populates="user", cascade="all, delete-orphan")

# attendance table
class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=True)
    total_hours = Column(Float, nullable=True)
    on_leave = Column(Boolean, default=False)
    break_start = Column(DateTime, nullable=True)
    break_end = Column(DateTime, nullable=True)
    total_break = Column(Float, nullable=True)

    user = relationship("User", back_populates="attendances")