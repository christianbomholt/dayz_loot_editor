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
        print("DEBUG the database is connected and session made")

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
        item.tier = updated_item.tier
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
        #print("DEBUG :", sql_filter_items)        
        db_cursor.execute(sql_filter_items)
        items = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return items

    def getSubtypesMods(self, mod):
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        print("DEBUG in GetSubtupesMods: ", mod)
        sql_filter_items = f"SELECT subtype, mods FROM items WHERE mods='{mod}' group by subtype"
        print("DEBUG in GetSubtupesMods", sql_filter_items)
        db_cursor.execute(sql_filter_items)
        subtypes = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return [_[0] for _ in subtypes]    
  
    def fast_search_like_name(self, item_name):
        search = f'%{item_name}%'
        results = self.session.query(Item).filter(Item.name.like(search)).all()
        return [u.__dict__ for u in results]


    def items_table_exist(self):
        #print("DEBUG checking if table exist ", self.db_name)
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        sql_filter_items = f"SELECT name FROM sqlite_master WHERE type='table' AND name='items'"
        db_cursor.execute(sql_filter_items)
        tables = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return len(tables) == 1

    def sql_dbDump(self):
        s =  str(self.db_name).split(".")
        filename = f"../{s[0]}.sql"
        db_connection = sqlite3.connect(self.db_name)
        with open(filename, 'w') as f:
            for line in db_connection.iterdump():
                f.write('%s\n' % line)


#Trying to make the setprices work...............
    # name, subtype, tradercat, buyprice, sellprice, rarity, nominal, traderexclude, mod
    def getSubtypeForTrader(self, subtype):
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        sql_filter_items = f"select name, subtype, tradercat, buyprice, sellprice, rarity, nominal, traderexclude, mod from items where subtype = '{subtype}'"
        db_cursor.execute(sql_filter_items)
        result = db_cursor.fetchall()
        for i in range(len(result)):
            if result[i][3] is None:
                result[i][3] = -1
            if result[i][4] is None:
                result[i][4] = -1
            result[i] = list(result[i])
        return result

    def getItemDetailsByTraderLoc(self, subtype, trader_loc):
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        query = f'SELECT name FROM items where trader_loc = {trader_loc} and subtype = "{subtype}"'
        db_cursor.execute(query)
        results = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return [row[0] for row in results]


    def getTraderLocsBySubtype(self, subtype):
        db_connection = sqlite3.connect(self.db_name)
        db_cursor = db_connection.cursor()
        query = f"SELECT trader_loc FROM items WHERE subtype = '{subtype}' group by trader_loc"
        db_cursor.execute(query)
        results = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        results = [row[0] if row[0] is not None else "" for row in results]
        return sorted(results)

    def setSubtypeForTrader_fast(self, names, cat, bprice, sprice, exclude, rarity):
        self.session.query(Item).filter(
            Item.name.in_(names)
        ).update({
            Item.traderCat: cat,
            Item.buyprice: cat,
            Item.sellprice: cat,
            Item.traderExclude: exclude,
            Item.rarity: rarity
        }, synchronize_session=False)
        self.session.commit()

    # def setSubtypeForTrader(self, items):
    #     db_connection = sqlite3.connect(self.db_name)
    #     db_cursor = db_connection.cursor()
    #     sql_set_items = f"UPDATE items SET traderCat = ?, buyprice = ?, sellprice= ?, traderExclude= ?, rarity= ? WHERE name = ?;", items"
    #     db_cursor.executemany(sql_set_items, items)
    #     db_connection.commit()
    #     db_connection.close()              