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
        Column("rarity", String),
        Column("item_type", String),
        Column("sub_type", String),
        Column("mod", String),
        Column("trader", Integer),
        Column("dynamic_event", Integer),
        Column("count_in_hoarder", Integer),
        Column("count_in_cargo", Integer),
        Column("count_in_player", Integer),
        Column("count_in_map", Integer),
    )

    def __init__(self, db_name):
        engine = create_engine(f"sqlite:///{db_name}")
        self.meta.create_all(engine)
