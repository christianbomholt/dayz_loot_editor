from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
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
    tier = Column(String)
    rarity = Column(String, default = "undefined")
    cat_type = Column(String)
    item_type = Column(String)
    sub_type = Column(String)
    mod = Column(String, default="Vanilla")
    trader = Column(String, default="Trader1")
    dynamic_event = Column(Integer)
    count_in_cargo = Column(Integer)
    count_in_hoarder = Column(Integer)
    count_in_map = Column(Integer)
    count_in_player = Column(Integer)
    buyprice = Column(Integer, nullable=True)
    sellprice = Column(Integer, nullable=True)
    traderExclude = Column(Integer, default=0)
    traderCat = Column(String, nullable=True)


    def __repr__(self):
        return f"Items(id={self.id},name={self.name},nominal={self.nominal},min={self.min},restock={self.restock},\
        lifetime={self.lifetime},usage={self.usage},tier={self.tier},rarity={self.rarity},cat_type={self.cat_type},\
        item_type={self.item_type},sub_type={self.sub_type},mod={self.mod},trader={self.trader},dynamic_event={self.dynamic_event},\
        count_in_cargo={self.count_in_cargo},count_in_hourder={self.count_in_hoarder},count_in_map={self.count_in_map},\
        count_in_player={self.count_in_player},buyprice={self.buyprice},sellprice={self.sellprice},traderExclude={self.traderExclude},\
        traderCat={self.traderCat})"
