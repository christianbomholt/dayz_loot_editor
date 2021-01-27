from sqlalchemy import create_engine, MetaData, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

def init_database(db_name):
    engine = create_engine(f"sqlite:///{db_name}")
    Base.metadata.create_all(engine)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    nominal = Column(Integer, default = 0)
    min = Column(Integer, default = 0)
    restock = Column(Integer, default = 1800)
    lifetime = Column(Integer, default = 38000)
    usage = Column(String)
    tier = Column(String)
    rarity = Column(String, default = "undefined")
    cat_type = Column(String)
    item_type = Column(String)
    sub_type = Column(String)
    mod = Column(String, default="Vanilla")
    trader = Column(String, default="Trader 1")
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


class Mapselect(Base):
    __tablename__ = "mapselect"
    id = Column(Integer, primary_key=True)
    mapselectvalue = Column(String)


class Attachments(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True)
    attachname = Column(String)

class Bullets(Base):
    __tablename__ = "bullets"
    id = Column(Integer, primary_key=True)
    bulletname = Column(String)
    bulletcount = Column(Integer)

class Magazines(Base):
    __tablename__ = "magazines"
    id = Column(Integer, primary_key=True)
    magname = Column(String)
    magbulletcount = Column(Integer)

    """
             "name": "CZ527_Camo",
            "attachments": [
                "GhillieAtt_ColorBase",
                "GhillieAtt_Tan",
                "GhillieAtt_Woodland",
                "GhillieAtt_Mossy",
                "HuntingOptic",
                "ImprovisedSuppressor"
            ],
            "bullets": [
                "Ammo_762x39",
                "Ammo_762x39Tracer"
            ],
            "magazines": [
                "Mag_CZ527_5rnd"
            ]"""   