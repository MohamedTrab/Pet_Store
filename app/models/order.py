from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.db import Base

class Order(Base):
    __tablename__ = 'orders'
    __bind_key__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_price = Column(Float)

    user = relationship("User", back_populates="orders")  # Many-to-One
    items = relationship("OrderItem", back_populates="order")  # One-to-Many


class OrderItem(Base):
    __tablename__ = 'order_items'
    __bind_key__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))
    quantity = Column(Integer)

    product = relationship("Product")  # Many-to-One
    order = relationship("Order", back_populates="items")  # Many-to-One
