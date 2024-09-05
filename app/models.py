from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Numeric, Index
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    added_by = Column(Integer, ForeignKey("admins.id"), nullable=False, server_default="1")
    image_url = Column(String, nullable=True)
    admin = relationship("Admin")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, server_default="False")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    itineraries = relationship("UserItinerary", back_populates="user")


class UserVerification(Base):
    __tablename__ = "user_verification"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    code = Column(String, nullable=False)
    user = relationship("User")


class UserItinerary(Base):
    __tablename__ = "user_itineraries"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="itineraries")
    itineraries = relationship("Itinerary", back_populates="user_itinerary")


class Province(Base):
    __tablename__ = 'provinces'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class District(Base):
    __tablename__ = 'districts'

    id = Column(Integer, primary_key=True, nullable=False)
    province_id = Column(Integer, ForeignKey("provinces.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    province = relationship("Province")

    __table_args__ = (
        Index('idx_district_province_id', 'province_id'),
    )


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    district = relationship("District")

    __table_args__ = (
        Index('idx_activity_district_id', 'district_id'),
    )


class HotelsAndRestaurant(Base):
    __tablename__ = 'hotels_and_restaurants'

    id = Column(Integer, primary_key=True, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    cuisine = Column(String, nullable=True)
    comfort = Column(String, nullable=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    price = Column(Numeric(10, 2), nullable=False, server_default="0.00")
    district = relationship("District")

    __table_args__ = (
        Index('idx_hotels_restaurants_district_id', 'district_id'),
    )


class Transportation(Base):
    __tablename__ = 'transportation'

    id = Column(Integer, primary_key=True, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    origin = Column(String, nullable=True, server_default=text("Not specified"))
    destination = Column(String, nullable=True, server_default=text("Not specified"))
    description = Column(String, nullable=True, server_default=text("Not specified"))
    departure = Column(String, nullable=True, server_default=text("Not specified"))
    arrival = Column(String, nullable=True, server_default=text("Not specified"))
    image_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    district = relationship("District")

    __table_args__ = (
        Index('idx_transportation_district_id', 'district_id'),
    )


class Attraction(Base):
    __tablename__ = 'attractions'

    id = Column(Integer, primary_key=True, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    district = relationship("District")
    price = Column(Numeric(10, 2), nullable=False, server_default="0.00")

    __table_args__ = (
        Index('idx_attraction_district_id', 'district_id'),
    )


class Itinerary(Base):
    __tablename__ = 'itineraries'

    id = Column(Integer, primary_key=True, nullable=False)
    user_itinerary_id = Column(Integer, ForeignKey("user_itineraries.id", ondelete="CASCADE"), nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    district = relationship("District")
    user_itinerary = relationship("UserItinerary", back_populates="itineraries")
    activities = relationship("ItineraryActivity", back_populates="itinerary")
    hotels_and_restaurants = relationship("ItineraryHotelRestaurant", back_populates="itinerary")
    transportations = relationship("ItineraryTransportation", back_populates="itinerary")
    attractions = relationship("ItineraryAttraction", back_populates="itinerary")


class ItineraryActivity(Base):
    __tablename__ = 'itinerary_activities'

    id = Column(Integer, primary_key=True, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)

    itinerary = relationship("Itinerary", back_populates="activities")
    activity = relationship("Activity")


class ItineraryHotelRestaurant(Base):
    __tablename__ = 'itinerary_hotels_restaurants'

    id = Column(Integer, primary_key=True, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    hotel_restaurant_id = Column(Integer, ForeignKey("hotels_and_restaurants.id", ondelete="CASCADE"), nullable=False)

    itinerary = relationship("Itinerary", back_populates="hotels_and_restaurants")
    hotel_restaurant = relationship("HotelsAndRestaurant")


class ItineraryTransportation(Base):
    __tablename__ = 'itinerary_transportations'

    id = Column(Integer, primary_key=True, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    transportation_id = Column(Integer, ForeignKey("transportation.id", ondelete="CASCADE"), nullable=False)

    itinerary = relationship("Itinerary", back_populates="transportations")
    transportation = relationship("Transportation")


class ItineraryAttraction(Base):
    __tablename__ = 'itinerary_attractions'

    id = Column(Integer, primary_key=True, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    attraction_id = Column(Integer, ForeignKey("attractions.id", ondelete="CASCADE"), nullable=False)

    itinerary = relationship("Itinerary", back_populates="attractions")
    attraction = relationship("Attraction")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
