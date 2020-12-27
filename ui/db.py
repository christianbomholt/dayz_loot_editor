from tkinter import Tk, Toplevel, Frame, StringVar, Radiobutton, Label, Entry, Button, filedialog

from database.init_db import InitDatabase
from config.ini_manager import INIManager
from database.dao import Dao


class DB(object):
    DATABASE_NAME = "dayz_items"
    INI_FILE = "app.ini"
    manage_ini = INIManager(INI_FILE)
    global DBname
    global newDataBase


    def openDB(self):
        DBname = filedialog.askopenfilename(filetypes=[("Sqlite db's", ".db")])
        newDataBase = False
        self.__start_db(False, DBname)

    def newDB(self):
        DBname = filedialog.asksaveasfilename(filetypes=[("Sqlite db's", ".db")])
        newDataBase = True
        self.__start_db(True, DBname)

    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.grab_set()

        self.configFrame = Frame(self.window)
        self.configFrame.grid(row=1, column=0, sticky="n,w,e", padx=30)

#        db_actions = [("New Database", "new"), ("Use Existing", "existing")]
#        self.selected_db_action = StringVar()
#        self.selected_db_action.set("existing")

#        Radiobutton(
#            self.configFrame,
#            text=db_actions[0][0],
#            variable=self.selected_db_action,
#            value=db_actions[0][1],
#        ).grid(row=6, column=0, pady=10)
#        Radiobutton(
#            self.configFrame,
#            text=db_actions[1][0],
#            variable=self.selected_db_action,
#            value=db_actions[1][1],
#        ).grid(row=6, column=1)

        Label(self.configFrame, text="Database Name").grid(row=7, column=0, sticky="w")

        self.db_name = StringVar()
        self.db_name.set(self.manage_ini.read_ini("Database", "Database_Name"))
#        self.db_name_entry = Entry(self.configFrame, textvariable= self.db_name)
#        self.db_name_entry = Entry(self.configFrame, textvariable= self.db_status)
#        self.db_name_entry.grid(row=7, column=1, sticky="e", pady=5)
        self.db_status = StringVar()
        self.db_status.set(
            "Database Connected to: "
            + self.manage_ini.read_ini("Database", "Database_Name")
        )

        Label(self.configFrame, textvariable=self.db_status).grid(
            columnspan=2, row=8, column=0, sticky="w"
        )
        button_frame = Frame(self.window)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        Button(
            button_frame, text="Init Database", width=12, command=self.__init_db
        ).grid(row=0, column=2, sticky="w", padx=5)
        Button(
            button_frame, text="Open DB", width=12, command=self.openDB
        ).grid(row=0, column=0, sticky="w", padx=5)
        Button(
            button_frame, text="New DB", width=12, command=self.newDB
        ).grid(row=0, column=1, sticky="w", padx=5)

        # windows.center(self.window)
        self.window.wait_window()


    def __start_db(self, new, DBname):
        if newDataBase:
            print("StartDB", DBname)
            InitDatabase(DBname)
            self.manage_ini.write_ini(
                section="Database",
                sub_section="Database_Name",
                value=DBname
            )
            self.db_status.set("Database connected to: " + DBname)
            print("DEBUG A New Database is being connected to ",DBname)
        else:
            if Dao(self.db_name.get()).items_table_exist(): # Dont quite understand what is checked in Items_table_exist()
                self.manage_ini.write_ini(
                    section="Database",
                    sub_section="Database_Name",
                    value=DBname
                )
                self.db_status.set(
                "Database connected to: " + DBname
            )
            else:
                self.db_status.set(
                    "items table doesn't exist! Please initialize your Database."
                )




    def __init_db(self):
       
        if len(self.db_status.get().split(".")) != 2:
            self.db_status.set("Incorrect! Please use DB name with .db extension.")
        else:
            if self.db_status.get().split(".")[1] != "db":
                self.db_status.set("Incorrect! Please use DB name with .db extension.")
            else:
                if self.newDataBase:
                    InitDatabase(DBname)
                    self.manage_ini.write_ini(
                        section="Database",
                        sub_section="Database_Name",
                        value=DBname,
                    )
                    self.db_status.set("Database connected to: " + DBname)
                else:
                    if Dao(DBname).items_table_exist(): # Dont quite understand what is checked in Items_table_exist()
                        self.manage_ini.write_ini(
                            section="Database",
                            sub_section="Database_Name",
                            value=DBname,
                        )
                        self.db_status.set(
                            "Database connected to: " + DBname
                        )
                    else:
                        self.db_status.set(
                            "items table doesn't exist! Please initialize your Database."
                        )


def testWindow():
    window = Tk()
    DB(window)
    window.mainloop()
