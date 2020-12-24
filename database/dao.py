import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.item import Item


class Dao(object):
    def __init__(self, db_name):
        self.db_name = db_name
        engine = create_engine(f"sqlite:///{db_name}")
        session_maker = sessionmaker()
        session_maker.configure(bind=engine)
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
            sql_filter_items = f"select * from items where sub_type='{item_sub_type}'" # Update to filter on Sub_type
            #sql_filter_items = f"select * from items where item_type = '{item_type}' AND sub_type='{item_sub_type}'"
            db_cursor.execute(sql_filter_items)
        else:
            sql_filter_items = f"select * from items where item_type = '{item_type}'"
            db_cursor.execute(sql_filter_items)
        items = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        print(sql_filter_items)
        return items

    def search_by_name(self, item_name):
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        sql_filter_items = f"select * from items where name = '{item_name}'"
        db_cursor.execute(sql_filter_items)
        items = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return items


    def search_like_name(self, item_name):
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        sql_filter_items = f"select * from items where name like '%{item_name}%'"
        print(sql_filter_items)        
        db_cursor.execute(sql_filter_items)
        items = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return items
    
    def fast_search_like_name(self, item_name):
        search = f'%{item_name}%'
        results = self.session.query(Item).filter(Item.name.like(search)).all()
        return [u.__dict__ for u in results]


    def items_table_exist(self):
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        sql_filter_items = f"SELECT name FROM sqlite_master WHERE type='table' AND name='items'"
        db_cursor.execute(sql_filter_items)
        tables = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return len(tables) == 1

    def getDicts(items):
        itemsListOfDicts = []
        for item in items:
            itemsListOfDicts.append(Dao.getDict(item))
        return itemsListOfDicts


    def getDict(item):
        dict = {}
        keys = getCoulumNames()
        for k in range(len(item)):
            key = keys[k]
            if key == "mods":
                key = "mod"
            if key.startswith("count_in_"):
                key = key[9:]
            dict[key] = item[k]
        return dict 

    def getFlags(self, item_id):
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        sql_filter_items = f"select dynamic_event, count_in_cargo, count_in_hoarder, count_in_map, count_in_player  from items where id = '{item_id}'"
        db_cursor.execute(sql_filter_items)
        items = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return items