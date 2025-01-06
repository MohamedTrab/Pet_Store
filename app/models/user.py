from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.db import Base

class User(Base):
    __tablename__ = 'users'
    __bind_key__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    address = Column(String)
    role = Column(String)

    cart = relationship("Cart", back_populates="user", uselist=False)  # One-to-One
    orders = relationship("Order", back_populates="user")  # One-to-Many
    reviews = relationship("Review", back_populates="user")  # One-to-Many
    pets = relationship("Pet", back_populates="user")  # One-to-Many
