from sqlalchemy import Column, Integer, String
from config.database import Base


class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
