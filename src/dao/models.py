from __future__ import annotations
from typing import List

from sqlalchemy import Column, String, Table, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from src.dao.database import Base


CategoryRent = Table(
    "category_rent",
    Base.metadata,
    Column("category_id",Integer,ForeignKey("category.id"),primary_key=True),
    Column("rent_id",Integer,ForeignKey("rent.id"),primary_key=True)
    )

class Category(Base):
    __tablename__ = "category"

    name:str = Column(String,nullable=False)
    description:str = Column(String,nullable=True)
    rents:Mapped[List[Rent]] = relationship("Rent",secondary=CategoryRent,back_populates="categories")

    def __repr__(self):
        return str(f"id:{self.id} name: {self.name}")

class Rent(Base):
    __tablename__="rent"

    name:str = Column(String,nullable=False)
    description:str = Column(String,nullable=True)
    img:str = Column(String,nullable=True)
    price_id:str = Column(Integer, ForeignKey("price.id"))
    price:Mapped[Price] = relationship("Price", back_populates="rents")
    categories:Mapped[List[Category]] = relationship("Category",secondary=CategoryRent,back_populates="rents")

    def __repr__(self):
        return str(f"id:{self.id} name: {self.name}")

class Price(Base):
    __tablename__ = "price"

    month:int = Column(Integer)
    two_week:int = Column(Integer)
    day:int = Column(Integer)
    currency:str = Column(String)
    rents:Mapped[List[Rent]] = relationship("Rent", back_populates="price")

    def __repr__(self):
        return str(f"day: {self.day}\ntwo week: {self.two_week}\nmonth: {self.month}\nprice: {self.currency}")


def __all_models__():
    return Category,Rent,Price,CategoryRent