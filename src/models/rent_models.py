from __future__ import annotations
from typing import List,Any

from aiogram_dialog.api.entities import MediaAttachment
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String, ForeignKey,Table
from sqlalchemy.orm import relationship,Mapped

class Base(DeclarativeBase): pass

CategoryRent = Table(
    "category_rent",
    Base.metadata,
    Column("category_id",Integer,ForeignKey("category.id"),primary_key=True),
    Column("rent_id",Integer,ForeignKey("rent.id"),primary_key=True)
    )

class Category(Base):
    __tablename__ = "category"

    id:int = Column(Integer, primary_key=True, index=True)
    name:str = Column(String)
    description:str = Column(String)
    rents:Mapped[List[Rent]] = relationship("Rent",secondary=CategoryRent,back_populates="categories")

class Rent(Base):
    __tablename__="rent"

    id:int = Column(Integer, primary_key=True, index=True)
    name:str = Column(String)
    description:str = Column(String)
    img:str = Column(String)
    price_id:str = Column(Integer, ForeignKey("price.id"))
    price:Mapped[Price] = relationship("Price", back_populates="rents")
    categories:Mapped[List[Category]] = relationship("Category",secondary=CategoryRent,back_populates="rents")

class Price(Base):
    __tablename__ = "price"

    id:int = Column(Integer, primary_key=True, index=True)
    month:int = Column(Integer)
    two_week:int = Column(Integer)
    day:int = Column(Integer)
    currency:str = Column(String)
    rents:Mapped[List[Rent]] = relationship("Rent", back_populates="price")

    def __repr__(self):
        return str(f"day: {self.day}\ntwo week: {self.two_week}\nmonth: {self.month}\nprice: {self.currency}")