from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Boolean, PrimaryKeyConstraint
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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, server_default="False")
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


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
