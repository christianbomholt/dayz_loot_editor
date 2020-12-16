from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    nominal = Column(Integer)
    min = Column(Integer)
    restock = Column(Integer)
    lifetime = Column(Integer)
    usage = Column(String)
    tire = Column(String)
    rarity = Column(String)
    item_type = Column(String)
    sub_type = Column(String)
    mod = Column(String)
    trader = Column(Integer)
    dynamic_event = Column(Integer)
    count_in_cargo = Column(Integer)
    count_in_hoarder = Column(Integer)
    count_in_map = Column(Integer)
    count_in_player = Column(Integer)
