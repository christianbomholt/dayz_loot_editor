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

    def upgradeDB(self):
        try:
            sql_String = f'ALTER TABLE items ADD COLUMN min_Stock INTEGER DEFAULT 10'
            self.session.execute(sql_String)
            self.session.commit()
            #print("DEBUG: The Column min_Stock added to database")
        except:
            pass

        try:
            sql_String = f'ALTER TABLE items ADD COLUMN max_Stock INTEGER DEFAULT 100'
            self.session.execute(sql_String)
            self.session.commit()
            #print("DEBUG: The Column max_stock added to database")
        except:
            print("DEBUG: You are good to go")

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

    def get_attach(self, attachClasse, item_id):
        item = self.session.query(attachClasse).get(item_id)
        self.session.commit()
        return item

# Used in a different filters

    def get_all_categories(self, col):
        result = self.session.query(Item).distinct(Item.cat_type)
        result = [c[0] for c in result if c[0] is not None]
        result.append("all")
        return result

    def flatten(t):
        return [item for sublist in t for item in sublist]

    def get_all_usage(self, col):
        result = self.session\
            .query(getattr(Item, col).distinct().label(col+'s'))\
            .order_by(desc(getattr(Item, col))).all()
        row_list = [c[0] for c in result if c[0] is not None]
        word_list = [i.split(',') for i in row_list]
        flattened_word_list = Dao.flatten(word_list)
        unique_word_list = list(sorted(set(flattened_word_list)))
        unique_word_list = list(filter(lambda x: x != "", unique_word_list))
        # unique_word_list.insert(0, "")
        # unique_word_list.append("all")
        return unique_word_list

    def get_all_types(self, col):
        result = self.session\
            .query(getattr(Item, col).distinct().label(col+'s'))\
            .order_by(desc(getattr(Item, col)))
        result = [c[0] for c in result if c[0] is not None]
        result.append("all")
        return result


# delete item - used in the delete button

    def delete_item(self, item_id):
        item = self.session.query(Item).get(item_id)
        self.session.delete(item)
        self.session.commit()
    # delete items


# delete item - used in the delete button

    def delete_attach(self, attachClasse, item_id):
        item = self.session.query(attachClasse).get(item_id)
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
    def getNominalByCat(self, grid_items, cat_type):
        grid_items = grid_items.subquery()
        result = self.session\
            .query(Item.cat_type, func.sum(Item.nominal))\
            .filter(Item.cat_type == cat_type)\
            .join(grid_items, Item.id == grid_items.c.id)\
            .group_by(Item.cat_type)\
            .all()
        return result

# used in __create_nominal_info
    def getNominalByType(self, grid_items, item_type):
        grid_items = grid_items.subquery()
        result = self.session\
            .query(Item.item_type, func.sum(Item.nominal))\
            .filter(Item.item_type == item_type)\
            .join(grid_items, Item.id == grid_items.c.id)\
            .group_by(Item.item_type)\
            .all()
        return result

# *******************Used for Filter section***********************************************
    def filterby_type(self, selected_mods, col, value):
        result = self.session.query(Item)\
            .filter(
                and_(
                    Item.mod.in_(selected_mods)),
            getattr(Item, col) == value
        )
        return result

    def search_like_name(self, item_name):
        search = f'%{item_name}%'
        results = self.session.query(Item).filter(Item.name.like(search)).all()
        return results

    def search_subtypeby_name(self, item_name):
        search = f'%{item_name}%'
        results = self.session.query(Item.name, Item.sub_type, Item.trader).filter(
            Item.name.like(search)).all()
        return results

    def search_attach_name(self, attachClasse, item_name):
        search = f'%{item_name}%'
        results = self.session.query(attachClasse).filter(
            attachClasse.name.like(search)).all()
        return results

    def search_attach_name(self, attachClasse, item_name):
        search = f'%{item_name}%'
        results = self.session.query(attachClasse).filter(
            attachClasse.name.like(search)).all()
        return results

    def sql_dbDump(self):
        s = str(self.db_name).split(".")
        filename = f"../{s[0]}.sql"
        db_connection = sqlite3.connect(self.db_name)
        with open(filename, 'w') as f:
            for line in db_connection.iterdump():
                line = line.replace('\u202c', '')
                f.write('%s\n' % line)

# ***********************Selects for Trader Prices ***************************************************
    def get_tradersubtypetupl(self, traderSel, selected_Mods):
        results = self.session.query(Item.sub_type).filter(and_(Item.trader == (
            traderSel), Item.mod.in_(selected_Mods))).group_by(Item.sub_type).order_by(Item.sub_type).all()
        results = [sub_type[0] for sub_type in results]
        return results

# Used in Set prices
    def get_traderpricingtupl(self, traderSel, sub_type, selected_Mods):
        results = self.session.query(Item.name, Item.sub_type, Item.traderCat, Item.buyprice, Item.sellprice, Item.rarity, Item.nominal, Item.traderExclude,
                                     Item.mod, Item.min_stock, Item.max_stock).filter(and_(Item.trader == (traderSel), Item.sub_type == (sub_type), Item.mod.in_(selected_Mods))).all()
        return results

# Used in Set prices
    def get_traderitemstupl(self, traderSel, sub_type, selected_Mods):
        results = self.session.query(Item).filter(and_(Item.trader == (traderSel), Item.sub_type == (
            sub_type), Item.mod.in_(selected_Mods))).order_by(Item.sub_type).all()
        return [u.__dict__ for u in results]

# Used in Set prices to save to DB
    def setTraderValues_fast(self, values):
        for value in values:
            self.session.query(Item).filter(
                Item.name == value[7]
            ).update({
                Item.traderCat: value[0],
                Item.buyprice: value[1],
                Item.sellprice: value[2],
                Item.traderExclude: value[3],
                Item.rarity: value[6],
                Item.min_stock: value[4],
                Item.max_stock: value[5]
            }, synchronize_session=False)
        self.session.commit()

# *******************Used for PyTest***********************************************
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
            map_object = Mapselect(
                mapselectvalue=value
            )
            self.session.add(map_object)
            self.session.commit()

    def get_mapselectValue(self, item_id):
        results = self.session.query(Mapselect).get(item_id)
        self.session.commit()
        return results


# Make Spawnable types

    def get_all_ranged(self):
        result = self.session.query(Item.name).filter(
            Item.item_type == "ranged")
        result = [c[0] for c in result if c[0] is not None]
        result.insert(0, "all")
        return result
