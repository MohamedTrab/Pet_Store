from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.db import Base

class Product(Base):
    __tablename__ = 'products'
    __bind_key__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    stock = Column(Integer)
    images = Column(String)  # Consider JSON for multiple images
    specifications = Column(String)  # Store as JSON or text

    category = relationship("Category", back_populates="products")  # Many-to-One
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")  # One-to-Many
