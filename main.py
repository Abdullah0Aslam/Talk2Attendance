from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional, List
from schemas import UserCreate, UserResponse, AttendanceCreate, AttendanceResponse
from helpers import calculate_hours, calculate_duration
from database import engine, get_db, Base
from models import User, Attendance

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance System")


@app.get("/")
def home():
    return {"message": "Attendance System API"}


@app.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    total_duration = calculate_duration(user.start_date, user.resign_date)
    
    new_user = User(
        name=user.name.title(),
        age=user.age,
        department=user.department,
        start_date=user.start_date,
        resign_date=user.resign_date,
        total_duration=total_duration
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.get("/users/", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    department: Optional[str] = None,
    db: Session = Depends(get_db)
):

    query = db.query(User)
    
    if department:
        query = query.filter(User.department == department)
    
    users = query.offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    total_duration = calculate_duration(user.start_date, user.resign_date)
    
    db_user.name = user.name.title()
    db_user.age = user.age
    db_user.department = user.department
    db_user.start_date = user.start_date
    db_user.resign_date = user.resign_date
    db_user.total_duration = total_duration
    db_user.updated_at = datetime.now()
    
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}


@app.post("/attendance/", response_model=AttendanceResponse, status_code=201)
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == attendance.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if attendance.check_out and attendance.check_out <= attendance.check_in:
        raise HTTPException(status_code=400, detail="check_out must be after check_in")
    
    if attendance.break_start and attendance.break_end:
        if attendance.break_end <= attendance.break_start:
            raise HTTPException(status_code=400, detail="break_end must be after break_start")
    
    total_hours = calculate_hours(attendance.check_in, attendance.check_out)
    total_break = calculate_hours(attendance.break_start, attendance.break_end)
    
    new_attendance = Attendance(
        user_id=attendance.user_id,
        check_in=attendance.check_in,
        check_out=attendance.check_out,
        total_hours=total_hours,
        on_leave=attendance.on_leave,
        break_start=attendance.break_start,
        break_end=attendance.break_end,
        total_break=total_break
    )
    
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    
    return new_attendance

@app.get("/attendance/", response_model=List[AttendanceResponse])
def get_all_attendance(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    
    records = db.query(Attendance).offset(skip).limit(limit).all()
    return records

@app.get("/attendance/{attendance_id}", response_model=AttendanceResponse)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    
    record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    return record

@app.put("/attendance/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    

    user = db.query(User).filter(User.id == attendance.user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if attendance.check_out and attendance.check_out <= attendance.check_in:
        raise HTTPException(status_code=400, detail="check_out must be after check_in")
    
    if attendance.break_start and attendance.break_end:
        if attendance.break_end <= attendance.break_start:
            raise HTTPException(status_code=400, detail="break_end must be after break_start")
    
    
    total_hours = calculate_hours(attendance.check_in, attendance.check_out)
    total_break = calculate_hours(attendance.break_start, attendance.break_end)
    
    # update fields
    db_attendance.user_id = attendance.user_id
    db_attendance.check_in = attendance.check_in
    db_attendance.check_out = attendance.check_out
    db_attendance.total_hours = total_hours
    db_attendance.on_leave = attendance.on_leave
    db_attendance.break_start = attendance.break_start
    db_attendance.break_end = attendance.break_end
    db_attendance.total_break = total_break
    
    # save changes
    db.commit()
    db.refresh(db_attendance)
    
    return db_attendance

@app.delete("/attendance/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):

    record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    db.delete(record)
    db.commit()
    
    return {"message": "Attendance record deleted successfully"}


