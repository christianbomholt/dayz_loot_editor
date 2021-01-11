import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, and_, func
from sqlalchemy.orm import sessionmaker
from model.item import Item


class Dao(object):
    databasename = ""
    def __init__(self, db_name):
        self.db_name = db_name
        Dao.databasename = db_name
        engine = create_engine(f"sqlite:///{db_name}")
        session_maker = sessionmaker()
        session_maker.configure(bind=engine)
        self.session = session_maker()
        #print("DEBUG the database is connected and session made")

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
    # get item used for __fill_entry_frame
    def get_item(self, item_id):
        item = self.session.query(Item).get(item_id)
        self.session.commit()
        return item
    """
    # get items
    def all_items(self):
        return self.session.query(Item)"""

    def get_allmods(self):
        result = self.session.query(Item.mod.distinct().label("mods"))
        self.session.commit()
        result=[mod[0] for mod in result if mod[0] is not None] 
        result.append("all")
        return result

    def get_all_types(self, col):
        result = self.session.query(getattr(Item, col).distinct().label(col+"s"))
        result=[c[0] for c in result if c[0] is not None]
        result.append("all")
        return result
    """    
    def get_allcat_types(self):
        result = self.session.query(Item.cat_type.distinct().label("cat_types"))
        self.session.commit()
        result=[cat_type[0] for cat_type in result if cat_type[0] is not None]
        result.append("all")
        return result

    def get_allitem_types(self):
        result = self.session.query(Item.item_type.distinct().label("cat_types"))
        self.session.commit()
        result=[item_type[0] for item_type in result if item_type[0] is not None]
        result.append("all")
        return result

    def get_allsub_types(self):
        result = self.session.query(Item.sub_type.distinct().label("sub_types"))
        self.session.commit()
        result= [sub_type[0] for sub_type in result if sub_type[0] is not None]
        result.append("all")
        return result"""

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

    def getNominal(self, grid_items):
        grid_items = grid_items.subquery()
        result = self.session\
            .query(func.sum(Item.nominal))\
            .join(grid_items, Item.id == grid_items.c.id)\
            .all()
        result = [x[0] for x in result]    
        return result       

    def getNominalByType(self, grid_items, item_type):
        grid_items = grid_items.subquery()
        result = self.session\
            .query(Item.item_type, func.sum(Item.nominal))\
            .join(grid_items, Item.id == grid_items.c.id)\
            .group_by(Item.item_type)\
            .all()
        return result 
#*******************Used for Filter section***********************************************

    def filterby_type(self, selected_mods, col,value):
        result = self.session.query(Item)\
            .filter(
                and_(
                    Item.mod.in_ (selected_mods)),
                    getattr(Item, col)==value
                )
        return result        

#*******************Used for PyTest***********************************************
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

#***********************Selects for Trader Prices ***************************************************
    def get_tradersubtypetupl(self, traderSel,selected_Mods):
        results = self.session.query(Item.sub_type).filter(and_(Item.trader==(traderSel),Item.mod.in_(selected_Mods))).group_by(Item.sub_type).order_by(Item.sub_type).all()
        results=[sub_type[0] for sub_type in results]
        return results
    """
#Trying to make the setprices work...............
    # name, subtype, tradercat, buyprice, sellprice, rarity, nominal, traderexclude, mod
    def getSubtypeForTrader(self, sub_type):
        db_connection = sqlite3.connect(Dao.databasename)
        db_cursor = db_connection.cursor()
        query = f"select name, sub_type, tradercat, buyprice, sellprice, rarity, nominal, traderexclude, mod from items where sub_type = '{sub_type}'"
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        result =  [list(elem) for elem in result]
        for i in range(len(result)):
            if result[i][3] is None:
                result[i][3] = -1
            if result[i][4] is None:
                result[i][4] = -1
            result[i] = list(result[i])
        return result"""

    def get_traderpricingtupl(self, traderSel, sub_type, selected_Mods):
        results = self.session.query(Item.name,Item.sub_type,Item.traderCat,Item.buyprice,Item.sellprice,Item.rarity,Item.nominal,Item.traderExclude,Item.mod).filter(and_(Item.trader==(traderSel),Item.sub_type==(sub_type),Item.mod.in_(selected_Mods))).all()
        return results

    def get_traderitemstupl(self, traderSel, sub_type, selected_Mods):
        results = self.session.query(Item).filter(and_(Item.trader==(traderSel),Item.sub_type==(sub_type),Item.mod.in_(selected_Mods))).all()
        return [u.__dict__ for u in results]
    """
    def getItemDetailsByTraderLoc(self, sub_type, trader):
        db_connection = sqlite3.connect(Dao.databasename)
        db_cursor = db_connection.cursor()
        query = f'SELECT name FROM items where trader = {trader} and sub_type = "{sub_type}"'
        db_cursor.execute(query)
        results = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        return [row[0] for row in results]


    def getTradersBySubtype(self, sub_type):
        db_connection = sqlite3.connect(Dao.databasename)
        db_cursor = db_connection.cursor()
        query = f"SELECT trader FROM items WHERE sub_type = '{sub_type}' group by trader"
        db_cursor.execute(query)
        results = db_cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        results = [row[0] if row[0] is not None else "" for row in results]
        return sorted(results)"""

    # traderCat, buyprice, sellprice, traderExclude, rarity, name
    def setSubtypeForTrader_fast(self, traderCat, buyprice, sellprice, traderExclude, rarity, name):
        self.session.query(Item).filter(
            Item.name.in_(name)
        ).update({
            Item.traderCat: traderCat,
            Item.buyprice: buyprice,
            Item.sellprice: sellprice,
            Item.traderExclude: traderExclude,
            Item.rarity: rarity
        }, synchronize_session=False)
        self.session.commit()

    def setTraderValues_fast(self, values):
        for value in values:
            self.session.query(Item).filter(
                Item.name==value[5]
            ).update({
                Item.traderCat: value[0],
                Item.buyprice: value[1],
                Item.sellprice: value[2],
                Item.traderExclude: value[3],
                Item.rarity: value[4]
            }, synchronize_session=False)
        self.session.commit()        

    def filtertoselectedmods(self,selected_Mods):
        result = self.session.query(Item).filter(Item.mod.in_ (selected_Mods))
        self.session.commit()
        return result

    #******************Distributor*****************************
    def getDicts(self, items):
        itemsListOfDicts = []
        for item in items:
            itemsListOfDicts.append(Dao.getDict(item))
        return itemsListOfDicts


    def getDict(self, item):
        dict = {}
        keys = Dao.getCoulumNames(item)
        for k in range(len(item)):
            key = keys[k]
            if key == "mods":
                key = "mod"
            if key.startswith("count_in_"):
                key = key[9:]
            dict[key] = item[k]
        return dict

    def getCoulumNames(self, item):
        return item.__table__.columns.keys()