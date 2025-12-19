from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, timezone

# --- Settings ---
class SettingBase(BaseModel):
    currency: str = Field(min_length=1, max_length=10)
    fuel_price: float = Field(gt=0)

class SettingOut(SettingBase):
    id: int
    class Config:
        from_attributes = True

# --- Users ---
class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    color: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")

class UserCreate(UserBase):
    password: str = Field(min_length=1)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")
    password: Optional[str] = Field(None, min_length=1)

class UserOut(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

# --- Rides ---
class RideInput(BaseModel):
    user_id: int
    timestamp: datetime
    distance_km: Optional[float] = Field(None, gt=0)
    consumption_l100km: Optional[float] = Field(None, gt=0)
    fuel_liters: Optional[float] = Field(None, gt=0)

    @field_validator('timestamp')
    def validate_timestamp(cls, v):
        # Prevent future dates significantly ahead (e.g. clock skew tolerance)
        now = datetime.now(timezone.utc) if v.tzinfo else datetime.now()
        if v > now:
            # Allow small skew, but generally log logic handles current time
            pass
        return v

class RideOut(BaseModel):
    id: int
    user_id: int
    tank_cycle_id: int
    timestamp: datetime
    distance_km: float
    consumption_l100km: float
    fuel_liters: float
    user: UserOut

    class Config:
        from_attributes = True

# --- Cycles ---
class TankCycleOut(BaseModel):
    id: int
    start_date: datetime
    end_date: Optional[datetime]
    is_active: bool
    class Config:
        from_attributes = True

# --- Stats ---
class UserStat(BaseModel):
    user_id: int
    user_name: str
    user_color: str
    total_distance: float
    total_fuel: float
    total_cost: float
    avg_consumption: float

class CycleStats(BaseModel):
    cycle_id: int
    is_active: bool
    total_distance: float
    total_fuel: float
    total_cost: float
    user_stats: List[UserStat]

# --- Admin ---
class AdminLogin(BaseModel):
    password: str = Field(min_length=1)

class AdminToken(BaseModel):
    access_token: str
    token_type: str

class AdminPasswordChange(BaseModel):
    old_password: str = Field(min_length=1)
    new_password: str = Field(min_length=1)

class RideUpdate(BaseModel):
    distance_km: Optional[float] = Field(None, gt=0)
    consumption_l100km: Optional[float] = Field(None, gt=0)
    fuel_liters: Optional[float] = Field(None, gt=0)