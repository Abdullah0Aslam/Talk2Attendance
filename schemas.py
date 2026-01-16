from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class UserCreate(BaseModel):
    name: str
    age: int
    department: str
    start_date: date
    resign_date: Optional[date] = None

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    department: str
    created_at: datetime
    updated_at: datetime
    start_date: date
    resign_date: Optional[date]
    total_duration: Optional[int]
    
    class Config:
        from_attributes = True

class AttendanceCreate(BaseModel):
    user_id: int
    check_in: datetime
    check_out: Optional[datetime] = None
    on_leave: bool = False
    break_start: Optional[datetime] = None
    break_end: Optional[datetime] = None

class AttendanceResponse(BaseModel):
    id: int
    user_id: int
    check_in: datetime
    check_out: Optional[datetime]
    total_hours: Optional[float]
    on_leave: bool
    break_start: Optional[datetime]
    break_end: Optional[datetime]
    total_break: Optional[float]
    
    class Config:
        from_attributes = True