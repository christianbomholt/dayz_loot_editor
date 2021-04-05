from sqlalchemy import create_engine, MetaData, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def init_database(db_name):
    engine = create_engine(f"sqlite:///{db_name}")
    Base.metadata.create_all(engine)
    return engine

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    nominal = Column(Integer, default = 0)
    min = Column(Integer, default = 0)
    qmin = Column(Integer, default = -1)
    qmax = Column(Integer, default = -1)
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
    min_stock = Column(Integer, nullable=True)
    max_stock = Column(Integer, nullable=True) 

    def __repr__(self):
        return f"Items(id={self.id},name={self.name},nominal={self.nominal},min={self.min},qmin={self.qmin},qmax={self.qmax},restock={self.restock},\
        lifetime={self.lifetime},usage={self.usage},tier={self.tier},rarity={self.rarity},cat_type={self.cat_type},\
        item_type={self.item_type},sub_type={self.sub_type},mod={self.mod},trader={self.trader},dynamic_event={self.dynamic_event},\
        count_in_cargo={self.count_in_cargo},count_in_hourder={self.count_in_hoarder},count_in_map={self.count_in_map},\
        count_in_player={self.count_in_player},buyprice={self.buyprice},sellprice={self.sellprice},traderExclude={self.traderExclude},\
        traderCat={self.traderCat},minStock={self.min_stock},maxStock={self.max_stock})"


class Mapselect(Base):
    __tablename__ = "mapselect"
    id = Column(Integer, primary_key=True)
    mapselectvalue = Column(String)

class LinkAttachments(Base):
    __tablename__ = "link_attachments"
    id = Column(Integer, primary_key=True)
    itemname = Column(String)
    attachname = Column(String)
    
    def __repr__(self):
        return f"Link(itemname={self.itemname}, attachname={self.attachname})"

class LinkMags(Base):
    __tablename__ = "link_mags"
    id = Column(Integer, primary_key=True)
    itemname = Column(String)
    magname = Column(String)    
    
class LinkBullets(Base):
    __tablename__ = "link_bullets"
    id = Column(Integer, primary_key=True)
    itemname = Column(String)
    bulletname = Column(String)

class LinkBulletMag(Base):
    __tablename__ = "link_bullet_to_mags"
    id = Column(Integer, primary_key=True)
    magname = Column(String)
    bulletname = Column(String)
    
class Attachments(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    attachcount = Column(Integer, default=7)
    prop = Column(Integer, default=0)
    def __repr__(self):
        return f"Attach(name={self.name}, attach_count={self.attachcount},attach_prop={self.prop})"

class Bullets(Base):
    __tablename__ = "bullets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    attachcount = Column(Integer, default=7)
    prop = Column(Integer, default=0)
    
    def __repr__(self):
        return f"Bullet(name={self.name}, bullet_count={self.attachcount},attach_prop={self.prop})"

class Magazines(Base):
    __tablename__ = "magazines"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    attachcount = Column(Integer, default=30)
    prop = Column(Integer, default=0)
    
    def __repr__(self):
        return f"Mag(name={self.name}, bullets_in_mag={self.attachcount},attach_prop={self.prop})"

class Ammobox(Base):
    __tablename__ = "ammobox"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    attachcount = Column(Integer, default=0)
    prop = Column(Integer, default=0)
    
    def __repr__(self):
        return f"Ammobox(name={self.name}, bullets_in_box={self.attachcount},ammobox_prop={self.prop})"        
