from tkinter import Tk, Toplevel, Frame, StringVar, Radiobutton, Label, Entry, Button, filedialog
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, and_, func
from sqlalchemy.orm import sessionmaker
from model.item import Item

from database.init_db import InitDatabase
from config.ini_manager import INIManager
from database.dao import Dao


class DB(object):
    DATABASE_NAME = "dayz_items"
    INI_FILE = "app.ini"
    manage_ini = INIManager(INI_FILE)

    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.grab_set()

        self.configFrame = Frame(self.window)
        self.configFrame.grid(row=1, column=0, sticky="n,w,e", padx=30)

        Label(self.configFrame, text="Database Name").grid(row=7, column=0, sticky="w")
        self.db_name = StringVar()
        self.db_name.set(self.manage_ini.read_ini("Database", "Database_Name"))
        self.db_status = StringVar()
        self.db_status.set(
            "Database Connected to: "
            + self.manage_ini.read_ini("Database", "Database_Name")
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
        db_path_name = filedialog.askopenfilename(filetypes=[("Sqlite db's", ".db")])
        if "/" in db_path_name:
            db_name = db_path_name.split("/")[-1]
        newDataBase = False
        self.__start_db(newDataBase, db_name)

    def newDB(self):
        db_path_name = filedialog.asksaveasfilename(filetypes=[("Sqlite db's", ".db")])
        if "/" in db_path_name:
            db_name = db_path_name.split("/")[-1]
        newDataBase = True
        self.__start_db(newDataBase, db_name)
        

    def __start_db(self, newDataBase, db_name):
        if newDataBase:
            InitDatabase(db_name)
            self.manage_ini.write_ini(
                section="Database",
                sub_section="Database_Name",
                value = db_name
            )
            self.db_status.set("Database connected to: " + db_name)
        else:
            if Dao(db_name).items_table_exist():
                self.manage_ini.write_ini(
                    section="Database",
                    sub_section="Database_Name",
                    value = db_name
                )
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
