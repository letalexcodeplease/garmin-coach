import os
from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, Date, JSON, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    garmin_id = Column(String, unique=True, nullable=False)
    activity_type = Column(String)
    name = Column(String)
    start_time = Column(DateTime)
    duration_seconds = Column(Float)
    distance_meters = Column(Float)
    avg_hr = Column(Float)
    max_hr = Column(Float)
    calories = Column(Float)
    avg_pace = Column(Float)
    elevation_gain = Column(Float)
    aerobic_te = Column(Float)  # Training Effect
    raw = Column(JSON)
    fetched_at = Column(DateTime, default=datetime.utcnow)

class Sleep(Base):
    __tablename__ = "sleep"

    id = Column(Integer, primary_key=True)
    date = Column(Date, unique=True, nullable=False)
    duration_seconds = Column(Float)
    deep_sleep_seconds = Column(Float)
    light_sleep_seconds = Column(Float)
    rem_sleep_seconds = Column(Float)
    awake_seconds = Column(Float)
    avg_spo2 = Column(Float)
    avg_stress = Column(Float)
    sleep_score = Column(Float)
    raw = Column(JSON)
    fetched_at = Column(DateTime, default=datetime.utcnow)

class DailyStats(Base):
    __tablename__ = "daily_stats"

    id = Column(Integer, primary_key=True)
    date = Column(Date, unique=True, nullable=False)
    steps = Column(Integer)
    calories_total = Column(Float)
    calories_active = Column(Float)
    avg_stress = Column(Float)
    max_stress = Column(Float)
    resting_hr = Column(Float)
    hrv_status = Column(String)
    body_battery_high = Column(Float)
    body_battery_low = Column(Float)
    raw = Column(JSON)
    fetched_at = Column(DateTime, default=datetime.utcnow)

_engine = None
_Session = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(os.getenv("DATABASE_URL"))
    return _engine

def get_session():
    global _Session
    if _Session is None:
        _Session = sessionmaker(bind=get_engine())
    return _Session()

def create_tables():
    Base.metadata.create_all(get_engine())
