from typing import Optional, Literal, List, Any
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


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


class HotelRestaurantBase(BaseModel):
    id: int
    type: str
    cuisine: str
    comfort: str
    title: str
    description: str
    created_at: datetime


class ItineraryHotelRestaurantsBase(BaseModel):
    id: int
    itinerary_id: int
    hotel_restaurant_id: int
    hotel_restaurant: HotelRestaurantBase


class TransportationBase(BaseModel):
    id: int
    type: Optional[str]
    origin: Optional[str]
    destination: Optional[str]
    description: Optional[str]
    departure: Optional[str]
    arrival: Optional[str]
    created_at: datetime


class ItineraryTransportationBase(BaseModel):
    id: int
    itinerary_id: int
    transportation_id: int
    transportation: TransportationBase


class AttractionsBase(BaseModel):
    id: int
    type: str
    title: str
    description: str
    created_at: datetime


class ItineraryAttractionsBase(BaseModel):
    id: int
    itinerary_id: int
    attraction_id: int
    attraction: AttractionsBase


class ItineraryBase(BaseModel):
    id: int
    user_itinerary_id: int
    district_id: int
    created_at: datetime


class ItineraryOut(ItineraryBase):
    district: DistrictBase
    activities: List[ItineraryActivityBase]
    hotels_and_restaurants: List[ItineraryHotelRestaurantsBase]
    transportations: List[ItineraryTransportationBase]
    attractions: List[ItineraryAttractionsBase]


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


class EntryBase(BaseModel):
    category: Literal[
        "transportations", "attractions", "activities", "hotels_and_restaurants", "districts", "provinces"]


# Creating schemas ---------------------------------------------------------------------------------------------------


class ProvinceCreate(BaseModel):
    title: str
    description: str


class DistrictCreate(BaseModel):
    province_id: int
    title: str
    description: str


class ActivityCreate(BaseModel):
    district_id: int
    title: str
    description: str


class ActivityOut(BaseModel):
    district_id: int
    title: str
    description: str
    created_at: datetime
    district: DistrictBase


class HotelsAndRestaurantsCreate(BaseModel):
    district_id: int
    type: str
    cuisine: str
    comfort: Literal["1", "2", "3", "4", "5"]
    title: str
    description: str


class TransportationCreate(BaseModel):
    district_id: int
    type: Literal["Bus", "Threewheeler", "bicycle", "motorcycle", "car", "train", "boat"]
    origin: Optional[str]
    destination: Optional[str]
    description: Optional[str]
    departure: Optional[str]
    arrival: Optional[str]


class AttractionsCreate(BaseModel):
    district_id: int
    type: str
    title: str
    description: str

