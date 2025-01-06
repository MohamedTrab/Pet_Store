from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.db import Base

class Cart(Base):
    __tablename__ = 'carts'
    __bind_key__ = 'users'
    

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="cart")  # One-to-One
    items = relationship("CartItem", back_populates="cart")  # One-to-Many


class CartItem(Base):
    __tablename__ = 'cart_items'
    __bind_key__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    cart_id = Column(Integer, ForeignKey('carts.id'))
    quantity = Column(Integer)

    product = relationship("Product")  # Many-to-One
    cart = relationship("Cart", back_populates="items")  # Many-to-One
