from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.db import Base

class Review(Base):
    __tablename__ = 'reviews'
    __bind_key__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Float)
    comment = Column(String)

    product = relationship("Product", back_populates="reviews")  # Many-to-One
    user = relationship("User", back_populates="reviews")  # Many-to-One
