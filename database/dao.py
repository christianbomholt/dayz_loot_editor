import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.item import Item


class DAO(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = create_engine(f"sqlite:///{db_name}")
        session_maker = sessionmaker()
        session_maker.configure(bind=self.engine)
        self.session = session_maker()

    """
    CRUD Operations related to items
    """

    # create item
    def create_item(self, item: Item, duplicate=0):
        if duplicate == 1:
            self.session.add(item)
            self.session.commit()
        else:
            if self.session.query(Item).filter(Item.name == item.name).count() == 0:
                self.session.add(item)
                self.session.commit()

    # update item
    def update_item(self, updated_item: Item):
        item = self.session.query(Item).get(updated_item.id)
        item.name = updated_item.name
        item.nominal = updated_item.nominal
        item.min = updated_item.min
        item.restock = updated_item.restock
        item.lifetime = updated_item.lifetime
        item.usage = updated_item.usage
        item.tire = updated_item.tire
        item.rarity = updated_item.rarity
        item.item_type = updated_item.item_type
        item.sub_type = updated_item.sub_type
        item.mod = updated_item.mod
        item.trader = updated_item.trader
        item.dynamic_event = updated_item.dynamic_event
        item.count_in_hoarder = updated_item.count_in_hoarder
        item.count_in_cargo = updated_item.count_in_cargo
        item.count_in_map = updated_item.count_in_map
        item.count_in_player = updated_item.count_in_player
        self.session.commit()

    # get item
    def get_item(self, item_id):
        item = self.session.query(Item).get(item_id)
        self.session.commit()
        return item

    # get items
    def all_items(self):
        """items = self.session.query(Item).all()
        self.session.commit()"""

        db_connection = sqlite3.connect(self.db_name)
        sql_delete_items = "select * from items"
        db_cursor = db_connection.cursor()
        db_cursor.execute(sql_delete_items)
        items = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return items

    def get_items(self):
        items = self.session.query(Item).all()
        self.session.commit()
        return items

    # delete item
    def delete_item(self, item_id):
        item = self.session.query(Item).get(item_id)
        self.session.delete(item)
        self.session.commit()

    # delete items
    def delete_items(self):
        db_connection = sqlite3.connect(self.db_name)
        sql_delete_items = "delete from items"
        db_cursor = db_connection.cursor()
        db_cursor.execute(sql_delete_items)
        db_connection.commit()
        db_connection.close()

    def filter_items(self, item_type, item_sub_type=None):
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        if item_sub_type is not None:
            sql_filter_items = "select * from items where item_type=? AND sub_type=?"
            db_cursor.execute(sql_filter_items, (item_type, item_sub_type))
        else:
            sql_filter_items = "select * from items where item_type=?"
            db_cursor.execute(sql_filter_items, (item_type,))
        items = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return items

    def search_by_name(self, item_name):
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        sql_filter_items = f"select * from items where name like '%{item_name}%'"
        db_cursor.execute(sql_filter_items)
        items = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return items
    
    def fast_search_by_name(self, item_name):
        search = f'%{item_name}%'
        # [u.__dict__ for u in results]
        return self.session.query(Item).filter(Item.name.like(search)).all()

    def items_table_exist(self):
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        sql_filter_items = "SELECT name FROM sqlite_master WHERE type= ? AND name=?"
        db_cursor.execute(sql_filter_items, ("table", "items"))
        tables = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return len(tables) == 1
