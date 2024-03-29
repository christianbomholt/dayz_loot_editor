from tkinter import messagebox
from database.dao import Dao
from tkinter import (
    Toplevel,
    Frame,
    Label,
    IntVar,
    StringVar,
    Checkbutton,
    Text,
    Radiobutton,
    Button,
    END,
    Tk,
    filedialog,
)
from tkinter import ttk
from config import ConfigManager
from xml_manager.xml_parser import XMLParser
import itertools as IT
from xml.etree import ElementTree as ET
import io

StringIO = io.StringIO


class NewItems(object):
    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.wm_title("Paste types")
        self.window.grab_set()
        self.config = ConfigManager("config.xml")
        self.database = Dao(self.config.get_database())
        self.mod_frame = Frame(self.window)
        self.mod_frame.grid(row=2, pady=3, sticky="w")
        Label(self.mod_frame, text="Enter Mod name:").grid(
            row=0, column=0, padx=3, pady=3
        )
        self.modSelector = ttk.Combobox(
            self.mod_frame, values=self.database.get_all_types("mod")
        )
        self.modSelector.set(self.database.get_all_types("mod")[0])
        self.modSelector.grid(row=0, column=1)
        self.duplicate = IntVar()
        self.duplicate.set(0)
        self.mapselectValue = StringVar()
        self.mapselectValue.set("Normal Map")

        Checkbutton(
            self.mod_frame,
            text="Use Values of Duplicate Items",
            variable=self.duplicate,
        ).grid(row=0, column=2, padx=10)

        self.text_area = Text(self.window)
        self.text_area.grid(row=1, padx=3, pady=3)

        self.buttons = Frame(self.window)
        Radiobutton(
            self.buttons,
            text="Normal Map",
            variable=self.mapselectValue,
            value="Normal Map",
        ).grid(row=3, column=0, sticky="w")
        Radiobutton(
            self.buttons,
            text="Namalsk",
            variable=self.mapselectValue,
            value="Namalsk Map",
        ).grid(row=3, column=1, sticky="w")

        self.buttons.grid(row=4, sticky="w")
        Button(
            self.buttons, text="OK", height=1, width=10, command=self.__add_items
        ).grid(padx=10, pady=10, column=0, row=4)
        Button(
            self.buttons, text="Open File", height=1, width=10, command=self.__open_file
        ).grid(padx=10, pady=10, column=1, row=4)

        self.window.wait_window()

    def __open_file(self):
        types_name = filedialog.askopenfilename(
            filetypes=[("Dayz types", ".xml")], defaultextension=".xml"
        )
        print(types_name)
        try:
            with open(types_name) as f:
                text = f.read()
                self.text_area.insert("1.0", text)
        except IOError:
            text = ""

    def __add_items(self):
        string_data = self.text_area.get(1.0, END).strip()
        if string_data == "":
            messagebox.showerror(
                title="Error", message="Empty Data", parent=self.window
            )
        else:
            try:
                # tree = ET.fromstring(string_data)
                xml_parser = XMLParser(string_data)
                items = xml_parser.get_items(self.mapselectValue.get())
                for i in items:
                    i.mod = self.modSelector.get()
                    print(i.name, i.mod)
                    self.database.create_item(item=i, duplicate=self.duplicate.get())
                self.window.destroy()

            except ET.ParseError as err:
                lineno, column = err.position
                line = next(IT.islice(StringIO(string_data), lineno))
                caret = "{:=>{}}".format("^", column)
                err.msg = "{}\n{}\n{}".format(err, line, caret)
                self.text_area.mark_set("insert", f"{lineno}.{column}")
                self.text_area.see("insert")
                self.text_area.focus()
                messagebox.showerror(
                    title="You have provided a xml that has errors",
                    message=err.msg,
                    parent=self.window,
                )


def testWindow():
    window = Tk()
    NewItems(window)
    window.mainloop()
