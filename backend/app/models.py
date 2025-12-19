from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String, default="CZK")
    fuel_price = Column(Float, default=35.50)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    color = Column(String)  # Hex code
    is_active = Column(Boolean, default=True)


class TankCycle(Base):
    __tablename__ = "tank_cycles"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    rides = relationship("Ride", back_populates="cycle")


class Ride(Base):
    __tablename__ = "rides"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tank_cycle_id = Column(Integer, ForeignKey("tank_cycles.id"))
    timestamp = Column(DateTime, default=datetime.now)

    distance_km = Column(Float)
    consumption_l100km = Column(Float)
    fuel_liters = Column(Float)

    # Relationships
    user = relationship("User")
    cycle = relationship("TankCycle", back_populates="rides")


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)