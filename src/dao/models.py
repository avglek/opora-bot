from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import Column, String, Table, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.dao.database import Base


CategoryRent = Table(
    "category_rent",
    Base.metadata,
    Column("category_id",Integer,ForeignKey("categories.id"),primary_key=True),
    Column("rent_id",Integer,ForeignKey("rents.id"),primary_key=True)
    )

class CategoryORM(Base):
    __tablename__ = "categories"

    name:Mapped[str] = mapped_column(String,nullable=False)
    description:Mapped[str] = mapped_column(String,nullable=True)
    rents:Mapped[List[RentORM]] = relationship("RentORM",secondary=CategoryRent,back_populates="categories")

    def __repr__(self):
        return str(f"id:{self.id} name: {self.name}")

class RentORM(Base):
    __tablename__="rents"

    name:Mapped[str] = mapped_column(String,nullable=False)
    description:Mapped[str] = mapped_column(String,nullable=True)
    img:Mapped[str] = mapped_column(String,nullable=False)
    price_id:Mapped[int] = mapped_column(ForeignKey("prices.id"))
    price:Mapped[PriceORM] = relationship("PriceORM", back_populates="rents")
    categories:Mapped[List[CategoryORM]] = relationship("CategoryORM",secondary=CategoryRent,back_populates="rents")
    orders:Mapped[List[OrderORM]] = relationship("OrderORM",backref="rents")

    def __repr__(self):
        return str(f"id:{self.id} name: {self.name}")

class PriceORM(Base):
    __tablename__ = "prices"

    month:Mapped[int] = mapped_column(Integer,nullable=True)
    two_week:Mapped[int] = mapped_column(Integer,nullable=True)
    day:Mapped[int] = mapped_column(Integer,nullable=True)
    currency:Mapped[int] = mapped_column(Integer,nullable=True)
    rents:Mapped[List[RentORM]] = relationship("RentORM", back_populates="price")

    def __repr__(self):
        return str(f"day: {self.day}\ntwo week: {self.two_week}\nmonth: {self.month}\nprice: {self.currency}")

class OrderORM(Base):
    __tablename__="orders"

    number:Mapped[str] = mapped_column(String,nullable=True)
    quantity:Mapped[int] = mapped_column(Integer,nullable=False)
    summa:Mapped[int] = mapped_column(Integer,nullable=True)
    period_id:Mapped[int] = mapped_column(Integer,nullable=False)
    rent_id:Mapped[int] = mapped_column(ForeignKey("rents.id"))
    rent:Mapped[RentORM] = relationship("RentORM",back_populates="orders",overlaps="rents")
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    user:Mapped[UserORM] = relationship("UserORM",back_populates="orders")
    create_dt:Mapped[datetime] = mapped_column(DATETIME,nullable=True)
    accept_dt:Mapped[datetime] = mapped_column(DATETIME,nullable=True)
    close_dt:Mapped[datetime] = mapped_column(DATETIME,nullable=True)


class UserORM(Base):
    __tablename__="users"

    name:Mapped[str] = mapped_column(String,nullable=False)
    email:Mapped[str] = mapped_column(String,nullable=True)
    firstname:Mapped[str] = mapped_column(String,nullable=True)
    lastname:Mapped[str] = mapped_column(String,nullable=True)
    telegram_id:Mapped[int] = mapped_column(Integer,nullable=False)
    orders:Mapped[List[OrderORM]] = relationship("OrderORM",back_populates="user")


def __all_models__():
    return CategoryORM,RentORM,PriceORM,CategoryRent,OrderORM,UserORM