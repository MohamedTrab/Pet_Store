from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.db import Base

class Category(Base):
    __tablename__ = 'categories'
    __bind_key__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    products = relationship("Product", back_populates="category")  # One-to-Many
