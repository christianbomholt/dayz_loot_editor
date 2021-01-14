"""
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String


class InitDatabase(object):
    meta = MetaData()
    items = Table(
        "items",
        meta,
        Column("id", Integer, primary_key=True),
        Column("name", String),
        Column("nominal", Integer),
        Column("min", Integer),
        Column("restock", Integer),
        Column("lifetime", Integer),
        Column("usage", String),
        Column("tier", String),
        Column("rarity", String, default = "undefined"),
        Column("cat_type", String),
        Column("item_type", String),
        Column("sub_type", String),
        Column("mod", String, default="Vanilla"),
        Column("trader", Integer),
        Column("dynamic_event", Integer),
        Column("count_in_cargo", Integer),
        Column("count_in_hoarder", Integer),
        Column("count_in_map", Integer),
        Column("buyprice", Integer, nullable=True),
        Column("count_in_player", Integer, nullable=True),
        Column("sellprice", Integer, default=0),
        Column("traderExclude", Integer, default=0),
        Column("traderCat", String, nullable=True),
        
    )
    def __init__(self, db_name):
        engine = create_engine(f"sqlite:///{db_name}")
        self.meta.create_all(engine)"""
        
