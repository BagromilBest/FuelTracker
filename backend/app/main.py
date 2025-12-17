from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
import os
from datetime import datetime

from . import models, schemas, database, logic

# Initialize DB
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="PiFuelTracker")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Dependencies ---
def get_db():
    return database.get_db()


# --- Helper ---
def ensure_settings(db: Session):
    settings = db.query(models.Setting).first()
    if not settings:
        settings = models.Setting()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


def get_active_cycle(db: Session):
    cycle = db.query(models.TankCycle).filter(models.TankCycle.is_active == True).first()
    if not cycle:
        cycle = models.TankCycle()
        db.add(cycle)
        db.commit()
        db.refresh(cycle)
    return cycle


# --- Routes ---

@app.get("/api/settings", response_model=schemas.SettingOut)
def read_settings(db: Session = Depends(database.get_db)):
    return ensure_settings(db)


@app.put("/api/settings", response_model=schemas.SettingOut)
def update_settings(settings: schemas.SettingBase, db: Session = Depends(database.get_db)):
    db_settings = ensure_settings(db)
    db_settings.currency = settings.currency
    db_settings.fuel_price = settings.fuel_price
    db.commit()
    db.refresh(db_settings)
    return db_settings


@app.get("/api/users", response_model=List[schemas.UserOut])
def read_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).filter(models.User.is_active == True).all()


@app.post("/api/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = models.User(name=user.name, color=user.color)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/api/rides", response_model=schemas.RideOut)
def create_ride(ride_in: schemas.RideInput, db: Session = Depends(database.get_db)):
    # 1. Calc/Validate Math
    d, c, f = logic.calculate_ride_data(ride_in.distance_km, ride_in.consumption_l100km, ride_in.fuel_liters)

    # 2. Get Active Cycle
    cycle = get_active_cycle(db)

    # 3. Save
    db_ride = models.Ride(
        user_id=ride_in.user_id,
        tank_cycle_id=cycle.id,
        timestamp=ride_in.timestamp,
        distance_km=d,
        consumption_l100km=c,
        fuel_liters=f
    )
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)
    return db_ride


@app.get("/api/cycles", response_model=List[schemas.TankCycleOut])
def get_cycles(db: Session = Depends(database.get_db)):
    return db.query(models.TankCycle).order_by(desc(models.TankCycle.start_date)).all()


@app.post("/api/cycles/close", response_model=schemas.TankCycleOut)
def close_cycle(db: Session = Depends(database.get_db)):
    cycle = get_active_cycle(db)
    cycle.is_active = False
    cycle.end_date = datetime.utcnow()

    new_cycle = models.TankCycle()  # Auto creates active=True
    db.add(new_cycle)

    db.commit()
    db.refresh(cycle)
    return cycle


@app.get("/api/stats", response_model=schemas.CycleStats)
def get_stats(cycle_id: Optional[int] = None, db: Session = Depends(database.get_db)):
    settings = ensure_settings(db)

    if cycle_id:
        cycle = db.query(models.TankCycle).filter(models.TankCycle.id == cycle_id).first()
        if not cycle: raise HTTPException(404, "Cycle not found")
    else:
        cycle = get_active_cycle(db)

    rides = db.query(models.Ride).filter(models.Ride.tank_cycle_id == cycle.id).all()

    # Aggregation
    total_dist = sum(r.distance_km for r in rides)
    total_fuel = sum(r.fuel_liters for r in rides)
    total_cost = total_fuel * settings.fuel_price

    user_map = {}
    users = db.query(models.User).all()

    for u in users:
        user_map[u.id] = {
            "user_id": u.id, "user_name": u.name, "user_color": u.color,
            "total_distance": 0.0, "total_fuel": 0.0, "total_cost": 0.0
        }

    for r in rides:
        if r.user_id in user_map:
            user_map[r.user_id]["total_distance"] += r.distance_km
            user_map[r.user_id]["total_fuel"] += r.fuel_liters

    # Finalize per user
    user_stats_list = []
    for uid, data in user_map.items():
        if data["total_distance"] > 0 or data["total_fuel"] > 0:
            data["total_cost"] = data["total_fuel"] * settings.fuel_price
            data["avg_consumption"] = (data["total_fuel"] * 100 / data["total_distance"]) if data[
                                                                                                 "total_distance"] > 0 else 0
            # Rounding
            data["total_distance"] = round(data["total_distance"], 2)
            data["total_fuel"] = round(data["total_fuel"], 2)
            data["total_cost"] = round(data["total_cost"], 2)
            data["avg_consumption"] = round(data["avg_consumption"], 2)
            user_stats_list.append(schemas.UserStat(**data))

    return schemas.CycleStats(
        cycle_id=cycle.id,
        is_active=cycle.is_active,
        total_distance=round(total_dist, 2),
        total_fuel=round(total_fuel, 2),
        total_cost=round(total_cost, 2),
        user_stats=user_stats_list
    )


# Static Files (Frontend)
# Ensure directory exists in production
if os.path.exists("../frontend/dist"):
    app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")