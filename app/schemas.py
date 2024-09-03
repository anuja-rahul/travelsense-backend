from typing import Optional, Literal, List, Any
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

from app.models import Province


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class AdminBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    created_at: datetime


class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class AdminOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str]


class ProvinceBase(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime


class DistrictBase(BaseModel):
    id: int
    province_id: int
    title: str
    description: str
    created_at: datetime

    province: ProvinceBase


class ActivityBase(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime


class ItineraryActivityBase(BaseModel):
    id: int
    itinerary_id: int
    activity_id: int
    activity: ActivityBase


class ItineraryBase(BaseModel):
    id: int
    user_itinerary_id: int
    district_id: int
    created_at: datetime


class ItineraryOut(ItineraryBase):
    district: DistrictBase
    activities: List[ItineraryActivityBase]
    # hotels_and_restaurants: Any
    # transportation: List[Any]
    # attractions: List[Any]


class UserItineraryBase(BaseModel):
    id: int
    user_id: int


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    verified: bool
    created_at: datetime
    itineraries: List[UserItineraryBase]

    class Config:
        from_attributes = True


class UserItineraryOut(BaseModel):
    id: int
    itineraries: List[ItineraryOut]


class UserLogin(BaseModel):
    email: EmailStr
    password: str
