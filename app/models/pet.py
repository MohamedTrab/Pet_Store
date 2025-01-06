from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.db import Base

class Pet(Base):
    __tablename__ = 'pets'
    __bind_key__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    age = Column(Integer)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="pets")  # Many-to-One
