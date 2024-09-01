from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, PrimaryKeyConstraint, Numeric, Index
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
    admin = relationship("Admin")


class Province(Base):
    __tablename__ = 'provinces'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class District(Base):
    __tablename__ = 'districts'

    id = Column(Integer, primary_key=True, nullable=False)
    province_id = Column(Integer, ForeignKey("provinces.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    province = relationship("Province")

    __table_args__ = (
        Index('idx_district_province_id', 'province_id'),
    )

    # __table_args__ = (
    #     PrimaryKeyConstraint('id', 'province_id', name='districts_pk'),
    # )


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    district = relationship("District")

    __table_args__ = (
        Index('idx_activity_district_id', 'district_id'),
    )

    # __table_args__ = (
    #         PrimaryKeyConstraint('id', 'district_id', name='activities_pk'),
    #     )


class HotelsAndRestaurant(Base):
    __tablename__ = 'hotels_and_restaurants'

    id = Column(Integer, primary_key=True, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    cuisine = Column(String, nullable=True)
    comfort = Column(String, nullable=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    district = relationship("District")

    __table_args__ = (
        Index('idx_hotels_restaurants_district_id', 'district_id'),
    )

    # __table_args__ = (
    #     PrimaryKeyConstraint("id", "district_id", name='hotels_and_restaurants_pk'),
    # )


class Transportation(Base):
    __tablename__ = 'transportation'

    id = Column(Integer, primary_key=True, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    description = Column(String, nullable=True)
    departure = Column(String, nullable=True)
    arrival = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    district = relationship("District")

    __table_args__ = (
        Index('idx_transportation_district_id', 'district_id'),
    )

    # __table_args__ = (
    #     PrimaryKeyConstraint('id', 'district_id', name='transportation_pk'),
    # )


class Attraction(Base):
    __tablename__ = 'attractions'

    id = Column(Integer, primary_key=True, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    district = relationship("District")

    __table_args__ = (
        Index('idx_attraction_district_id', 'district_id'),
    )

    # __table_args__ = (
    #     PrimaryKeyConstraint('id', 'district_id', name='attractions_pk'),
    # )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, server_default="False")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    itineraries = relationship("UserItinerary", back_populates="user")


class UserItinerary(Base):
    __tablename__ = "user_itineraries"

    id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="itineraries")

    __table_args__ = (
        PrimaryKeyConstraint('id', 'user_id', name='user_itinerary_pk'),
    )


class Itinerary(Base):
    __tablename__ = 'itineraries'

    id = Column(Integer, primary_key=True, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    district = relationship("District")
    activities = relationship("ItineraryActivity", backref="itinerary")
    hotels_and_restaurants = relationship("ItineraryHotelRestaurant", backref="itinerary")
    transportations = relationship("ItineraryTransportation", backref="itinerary")
    attractions = relationship("ItineraryAttraction", backref="itinerary")


class ItineraryActivity(Base):
    __tablename__ = 'itinerary_activities'

    id = Column(Integer, primary_key=True, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)

    itinerary = relationship("Itinerary", backref="itinerary_activities")
    activity = relationship("Activity")


class ItineraryHotelRestaurant(Base):
    __tablename__ = 'itinerary_hotels_restaurants'

    id = Column(Integer, primary_key=True, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    hotel_restaurant_id = Column(Integer, ForeignKey("hotels_and_restaurants.id", ondelete="CASCADE"), nullable=False)

    itinerary = relationship("Itinerary", backref="itinerary_hotels_restaurants")
    hotel_restaurant = relationship("HotelsAndRestaurant")


class ItineraryTransportation(Base):
    __tablename__ = 'itinerary_transportations'

    id = Column(Integer, primary_key=True, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    transportation_id = Column(Integer, ForeignKey("transportation.id", ondelete="CASCADE"), nullable=False)

    itinerary = relationship("Itinerary", backref="itinerary_transportations")
    transportation = relationship("Transportation")


class ItineraryAttraction(Base):
    __tablename__ = 'itinerary_attractions'

    id = Column(Integer, primary_key=True, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    attraction_id = Column(Integer, ForeignKey("attractions.id", ondelete="CASCADE"), nullable=False)

    itinerary = relationship("Itinerary", backref="itinerary_attractions")
    attraction = relationship("Attraction")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


# class UserCategory(Base):
#     __tablename__ = 'user_categories'
#
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
#     sub_category_id = Column(Integer, ForeignKey("subcategories.id", ondelete="CASCADE"), nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
#     user = relationship("User")
#     category = relationship("Category")
#     sub_category = relationship("SubCategory")
#
#     __table_args__ = (
#         PrimaryKeyConstraint('user_id', 'category_id', 'sub_category_id', name='user_category_pk')
#     )


# class SubCategory(Base):
#     __tablename__ = 'subcategories'
#
#     id = Column(Integer, primary_key=True, nullable=False)
#     category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, primary_key=True)
#     title = Column(String, nullable=False, unique=True)
#     description = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
#     added_by = Column(Integer, ForeignKey("admins.id"), nullable=False, server_default="1")
#     admin = relationship("Admin")
#     category = relationship("Category")
#
#     __table_args__ = (
#         PrimaryKeyConstraint('id', 'category_id', name='sub_category_pk')
#     )


# class Itinerary(Base):
#     __tablename__ = 'itineraries'
#
#     id = Column(Integer, ForeignKey(UserItinerary.id, ondelete="CASCADE"), nullable=False, primary_key=True)
#     district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
#     activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=True)
#     hotel_restaurant_id = Column(Integer, ForeignKey("hotels_and_restaurants.id", ondelete="CASCADE"), nullable=True)
#     transportation_id = Column(Integer, ForeignKey("transportation.id", ondelete="CASCADE"), nullable=True)
#     attraction_id = Column(Integer, ForeignKey("attractions.id", ondelete="CASCADE"), nullable=True)
#
#     itinerary_id = relationship("UserItinerary")
#     user = relationship("User")
#     district = relationship("District")
#     activity = relationship("Activity")
#     hotel_restaurant = relationship("HotelsAndRestaurant")
#     transportation = relationship("Transportation")
#     attraction = relationship("Attraction")
