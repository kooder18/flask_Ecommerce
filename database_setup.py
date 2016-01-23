import sys

from sqlalchemy import Column, ForeignKey, Integer, String


from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ ='category'
    name = Column(String(80), nullable = False)
    img = Column(String(180))
    id = Column(Integer, primary_key = True)

    @property
    def serialize(self):
        return {
        'name'      : self.name,
        'img'       : self.img,
        'id'        : self.id,
        }

class Item(Base):
    __tablename__ = 'item'
    name = Column(String(80), nullable = False)
    img  = Column(String(180))
    description = Column(String(180))
    id   = Column(Integer, primary_key = True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)


engine = create_engine('sqlite:///catalogue.db')

Base.metadata.create_all(engine)
