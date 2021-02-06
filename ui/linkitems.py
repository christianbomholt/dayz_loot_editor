from tkinter import Tk, Toplevel, Frame, StringVar, Radiobutton, Label, Entry, Button, filedialog,OptionMenu
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, and_, func
from sqlalchemy.orm import sessionmaker
from model.item import Item, init_database
from model.item import Mapselect,Attachments
from config import ConfigManager
from database.dao import Dao
from sqlalchemy.ext.declarative import declarative_base
import json



Base = declarative_base()

class LinkItem(object):

    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.grab_set()

        self.configFrame = Frame(self.window)
        self.configFrame.grid(row=3, column=0, sticky="n,w,e", padx=30)

        Label(self.configFrame, text="Select the LinkItems File:").grid(row=1, column=0, sticky="w")
# Buttons
        Button(
            self.configFrame, text="Open", width=12, command=self.openLinkItem
        ).grid(row=2, column=0, sticky="w", padx=5)
        self.window.wait_window()


    def openLinkItem(self):
        LinkItemFile = filedialog.askopenfilename(filetypes=[("DumpAttach", ".json")],defaultextension=".json")
        if "/" in LinkItemFile:
            LinkItemFile = LinkItemFile.split("/")[-1]       
        self.__loadLinkItem(LinkItemFile)


    def __loadLinkItem(self,LinkItemFile):
        with open(LinkItemFile, 'r') as myfile:
            data=myfile.read()
        attachments = json.loads(data)["HlyngeWeapons"]


def testWindow():
    window = Tk()
    LinkItem(window)
    window.mainloop()
