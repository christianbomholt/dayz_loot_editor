from tkinter import Tk, Toplevel, Frame, StringVar, Label, Button, filedialog, OptionMenu
from config import ConfigManager
from database.dao import Dao
from model.item import init_database

# Base = declarative_base()


class DB(object):

    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.grab_set()
        self.config = ConfigManager("config.xml")
        self.database = Dao(self.config.get_database())
        self.database_name = self.config.get_database()
        self.mapselectValue = StringVar()

        self.configFrame = Frame(self.window)
        self.configFrame.grid(row=3, column=0, sticky="n,w,e", padx=30)

        Label(self.configFrame, text="Database Name:").grid(
            row=1, column=0, sticky="w")
        self.db_name = StringVar()
        self.db_name.set(self.database_name)
        self.db_status = StringVar()
        self.db_status.set(f"{self.database_name}")
        Label(self.configFrame, textvariable=self.db_status).grid(
            columnspan=2, row=2, column=0, sticky="w"
        )
        self.db_name = self.db_status
        button_frame = Frame(self.window)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
# Selections
        self.DbInitValue = StringVar()
        optionList = ('Chernarus', 'Livonia',
                      'Namalsk', 'Deerisle', 'Chiemsee')
        self.DbInitValue.set(optionList[0])
        self.DbInit = OptionMenu(
            button_frame, self.DbInitValue, *optionList
        ).grid(row=4, column=1, sticky="w")
        db_map_name = self.database.get_mapselectValue(1).mapselectvalue
        self.DbInitValue.set(db_map_name)
        

# Buttons
        Button(
            button_frame, text="Open DB", width=12, command=self.openDB
        ).grid(row=6, column=0, sticky="w", padx=5)
        Button(
            button_frame, text="New DB", width=12, command=self.newDB
        ).grid(row=6, column=1, sticky="w", padx=5)
        self.window.wait_window()

    def openDB(self):
        db_name = filedialog.askopenfilename(
            filetypes=[("Sqlite db's", ".db")], defaultextension=".db")
        if "/" in db_name:
            db_name = db_name.split("/")[-1]
            self.db_status.set("Database connected to: " + db_name)
        newDataBase = False
        self.__start_db(newDataBase, db_name)

    def newDB(self):
        db_name = filedialog.asksaveasfilename(
            filetypes=[("Sqlite db's", ".db")], defaultextension=".db")
        if "/" in db_name:
            db_name = db_name.split("/")[-1]
        newDataBase = True
        self.__start_db(newDataBase, db_name)

    def __start_db(self, newDataBase, db_name):
        if newDataBase:
            # init_database(db_name)
            engine = init_database(db_name)
            # engine = create_engine(f"sqlite:///{db_name}")
            # Base.metadata.create_all(engine)
            raw_connection = engine.raw_connection()
            mapinit = self.DbInitValue.get()
            c = raw_connection.cursor()
            nrows = 0
            if engine.has_table("items"):
                c.execute("select count(*) from items")
                nrows = c.fetchall()[0][0]
            if nrows == 0:
                print(f"Initializing rows using '{mapinit}.sql'")
                raw_connection.cursor().executescript(
                    open(f"{mapinit}.sql").read())
                c.execute("select count(*) from items")
                nrows = c.fetchall()[0][0]
                print(f"Inserted { nrows } in the database")
            raw_connection.commit()
            init_database(db_name)
            Dao(db_name).setmapselectValue(mapinit)
            self.config.set_database(db_name)
            self.db_status.set("Database being loaded is: " + db_name)
            self.window.destroy()
        else:
            if Dao(db_name).items_table_exist():
                self.config.set_database(db_name)
                # self.DbInitValue.set(Dao(self.database_name).get_mapselectValue(1).mapselectvalue)
                self.db_status.set("We are opening: " + db_name)
                self.window.destroy()
            else:
                self.db_status.set(
                    "items table doesn't exist! Please initialize your Database.")


def testWindow():
    window = Tk()
    DB(window)
    window.mainloop()
