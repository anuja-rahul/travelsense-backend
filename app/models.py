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

    # __table_args__ = (
    #     Index('idx_district_title', 'title'),
    # )

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
