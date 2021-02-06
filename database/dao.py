import sqlite3
from sqlalchemy import create_engine, and_, func, desc, asc
from sqlalchemy.orm import sessionmaker
from model.item import Item, Mapselect


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

# create item  - used in new_items.py
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

#Used in a different filters
    
    def get_all_categories(self, col):
        result = self.session.query(Item).distinct(Item.category)
        result=[c[0] for c in result if c[0] is not None]
        result.append("all")
        return result
    """
    def get_all_types(self, col):
        result = self.session.query(getattr(Item, col).order_by(getattr(Item, col)).distinct().label(col+"s"))
        result=[c[0] for c in result if c[0] is not None]
        result.append("all")
        return result"""     

    def get_all_types(self, col):
        result = self.session\
            .query(getattr(Item,col).distinct().label(col+'s'))\
            .order_by(desc(getattr(Item,col)))
        result=[c[0] for c in result if c[0] is not None]
        result.append("all")
        return result     
    

# delete item - used in the delete button
    def delete_item(self, item_id):
        item = self.session.query(Item).get(item_id)
        self.session.delete(item)
        self.session.commit()

    # delete items
    
# Used in __create_nominal_info
    def getNominal(self, grid_items):
        grid_items = grid_items.subquery()
        result = self.session\
            .query(func.sum(Item.nominal))\
            .join(grid_items, Item.id == grid_items.c.id)\
            .all()
        result = [x[0] for x in result]    
        return result       

# used in __create_nominal_info
    def getNominalByType(self, grid_items, item_type):
        grid_items = grid_items.subquery()
        result = self.session\
            .query(Item.item_type, func.sum(Item.nominal))\
            .filter(Item.item_type==item_type)\
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

    def search_like_name(self, item_name):
        search = f'%{item_name}%'
        results = self.session.query(Item).filter(Item.name.like(search)).all()
        return results

    def sql_dbDump(self):
        s =  str(self.db_name).split(".")
        filename = f"../{s[0]}.sql"
        db_connection = sqlite3.connect(self.db_name)
        with open(filename, 'w') as f:
            for line in db_connection.iterdump():
                line = line.replace('\u202c', '')
                f.write('%s\n' % line)

#***********************Selects for Trader Prices ***************************************************
    def get_tradersubtypetupl(self, traderSel,selected_Mods):
        results = self.session.query(Item.sub_type).filter(and_(Item.trader==(traderSel),Item.mod.in_(selected_Mods))).group_by(Item.sub_type).order_by(Item.sub_type).all()
        results=[sub_type[0] for sub_type in results]
        return results
# Used in Set prices
    def get_traderpricingtupl(self, traderSel, sub_type, selected_Mods):
        results = self.session.query(Item.name,Item.sub_type,Item.traderCat,Item.buyprice,Item.sellprice,Item.rarity,Item.nominal,Item.traderExclude,Item.mod).filter(and_(Item.trader==(traderSel),Item.sub_type==(sub_type),Item.mod.in_(selected_Mods))).all()
        return results
# Used in Set prices
    def get_traderitemstupl(self, traderSel, sub_type, selected_Mods):
        results = self.session.query(Item).filter(and_(Item.trader==(traderSel),Item.sub_type==(sub_type),Item.mod.in_(selected_Mods))).order_by(Item.sub_type).all()
        return [u.__dict__ for u in results]
# Used in Set prices to save to DB
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

#*******************Used for PyTest***********************************************
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

    def setmapselectValue(self, value):
        exists = self.session.query(Mapselect).first()
        if not exists:
            print("DEBUG  setmapselectValue:",value )
            map_object = Mapselect(
                mapselectvalue = value
            )
            self.session.add(map_object)
            self.session.commit()   


    def get_mapselectValue(self,item_id):
        results = self.session.query(Mapselect).get(item_id)
        self.session.commit()
        return results      