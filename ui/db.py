from tkinter import Tk, Toplevel, Frame, StringVar, Radiobutton, Label, Entry, Button, filedialog
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, and_, func
from sqlalchemy.orm import sessionmaker
from model.item import Item

#from database.init_db import InitDatabase

from config import ConfigManager
from database.dao import Dao


class DB(object):

    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.grab_set()
        self.config = ConfigManager("config.xml")
        self.database_name = self.config.get_database()

        self.configFrame = Frame(self.window)
        self.configFrame.grid(row=1, column=0, sticky="n,w,e", padx=30)

        Label(self.configFrame, text="Database Name").grid(row=7, column=0, sticky="w")
        self.db_name = StringVar()
        self.db_name.set(self.database_name)
        self.db_status = StringVar()
        self.db_status.set(
            f"Database Connected to: {self.database_name}"
        )

        Label(self.configFrame, textvariable=self.db_status).grid(
            columnspan=2, row=8, column=0, sticky="w"
        )
        self.db_name = self.db_status
        button_frame = Frame(self.window)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        Button(
            button_frame, text="Open DB", width=12, command=self.openDB
        ).grid(row=0, column=0, sticky="w", padx=5)
        Button(
            button_frame, text="New DB", width=12, command=self.newDB
        ).grid(row=0, column=1, sticky="w", padx=5)

        self.window.wait_window()

    def openDB(self):
        db_name = filedialog.askopenfilename(filetypes=[("Sqlite db's", ".db")])
        if "/" in db_name:
            db_name = db_name.split("/")[-1]       
            self.db_status.set("Database connected to: " + db_name)

        newDataBase = False
        self.__start_db(newDataBase, db_name)

    def newDB(self):
        db_name = filedialog.asksaveasfilename(filetypes=[("Sqlite db's", ".db")])
        if "/" in db_name:
            db_name = db_name.split("/")[-1]
        newDataBase = True
        self.__start_db(newDataBase, db_name)
        

    def __start_db(self, newDataBase, db_name):
        if newDataBase:
            #InitDatabase(db_name)
            Item(db_name)
            self.config.set_database(db_name)
            self.db_status.set("Database connected to: " + db_name)
            engine = create_engine(f"sqlite:///{db_name}")
            Base.metadata.create_all(engine)
            raw_connection = engine.raw_connection()
            c = raw_connection.cursor()
            c.execute("select count(*) from items")
            nrows = c.fetchall()[0][0]

            print(f"number of rows in database: { nrows }")
            if nrows == 0:
                print(f"Initializing rows using 'init.sql'")
                raw_connection.cursor().executescript(open("../init.sql").read())
                c.execute("select count(*) from items")
                nrows = c.fetchall()[0][0]
                print(f"Inserted { nrows } in the database")
            raw_connection.commit()
        else:
            if Dao(db_name).items_table_exist():

                self.config.set_database(db_name)
                # self.manage_ini.write_ini(
                #     section="Database",
                #     sub_section="Database_Name",
                #     value = db_name
                # )
                self.db_status.set(
                "Database connected to: " + db_name
                )
            else:
                self.db_status.set(
                    "items table doesn't exist! Please initialize your Database."
                )


def testWindow():
    window = Tk()
    DB(window)
    window.mainloop()
