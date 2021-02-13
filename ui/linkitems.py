from tkinter import Tk, Toplevel, Frame, StringVar, Radiobutton, Label, Entry, Button, filedialog,OptionMenu, IntVar
from tkinter import ttk, VERTICAL, HORIZONTAL, LabelFrame,Tcl
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, and_, func
from sqlalchemy.orm import sessionmaker
from model.item import Item, init_database
from model.item import Mapselect,Attachments,LinkAttachments,LinkBulletMag,LinkBullets,LinkMags,Magazines,Bullets
from config import ConfigManager
from database.dao import Dao
from sqlalchemy.ext.declarative import declarative_base
import json
import re
from utility import attach_definition


Base = declarative_base()

class LinkItem(object):

    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.grab_set()
        self.config = ConfigManager("config.xml")
        self.database = Dao(self.config.get_database())
        self.__create_entry_frame()
        self.__create_tree_view()


    def __create_entry_frame(self):
        self.entryFrameHolder = Frame(self.window)
        self.entryFrameHolder.grid(row=0, column=0, sticky="nw")
        self.entryFrame = Frame(self.entryFrameHolder)
        self.entryFrame.grid(padx=8, pady=6)
        # labels
        Label(self.entryFrame, text="Name").grid(row=0, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Count").grid(row=1, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Prop").grid(row=2, column=0, sticky="w", pady=5)

        # input variables
        self.id = IntVar()
        self.name = StringVar()
        self.count = IntVar()
        self.prop = IntVar()
        
        # form fields
        self.nameField = Entry(self.entryFrame, textvariable=self.name)
        self.nameField.grid(row=0, column=1, sticky="w")
        self.countField = Entry(self.entryFrame, textvariable=self.count)
        self.countField.grid(row=1, column=1, sticky="w")
        self.propField = Entry(self.entryFrame, textvariable=self.prop)
        self.propField.grid(row=2, column=1, sticky="w")

        Button(
            self.entryFrame, text="Update", width=8, command=self.__update_item
        ).grid(row=5, column=0, pady=5, sticky="w")

        Button(
            self.entryFrame, text="Delete", width=8, command=self.__delete_item
        ).grid(row=5, column=1, pady=5, sticky="w")

        #self.configFrame = Frame(self.window)
        self.configFrame = Frame(self.entryFrameHolder)
        self.configFrame.grid(row=2, column=0, sticky="n,w,e", padx=30)
        Label(self.configFrame, text="Select the LinkItems File:").grid(row=1, column=0, sticky="w")
# Buttons
        Button(
            self.configFrame, text="Open", width=12, command=self.openLinkItem
        ).grid(row=2, column=0, sticky="n,w", padx=10)

    def __create_tree_view(self):
        style = ttk.Style()
        style.configure('Treeview', background='#97FFFF',foreground='black')

        self.treeFrame = Frame(self.window)
        self.treeFrame.grid(row=0, column=1, sticky="nsew")
        self.treeFrame.grid_rowconfigure(0, weight=1)
        self.treeFrame.grid_columnconfigure(1, weight=1)

        self.tree = ttk.Treeview(self.treeFrame, columns=[col.get("text") for col in attach_definition], height=40)
        style.map("Treeview",
                foreground=self.fixed_map(style,"foreground"),
                background=self.fixed_map(style,"background"))
        for col in attach_definition:
            self.tree.heading(
                col.get("col_id"),
                text=col.get("text"),
                command=lambda _col=col.get("text"): self.tree_view_sort_column(
                    self.tree, _col, False
                ),
            )
            self.tree.column(
                col.get("col_id"), 
                width=col.get("width"), 
                stretch=col.get("stretch")
            )
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.heading('#0', text='ID')
        self.tree.column('#0', width ="60", stretch="NO")
        self.treeView = self.tree
        vertical = ttk.Scrollbar(self.treeFrame, orient=VERTICAL)
        horizontal = ttk.Scrollbar(self.treeFrame, orient=HORIZONTAL)
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="we")
        self.tree.config(yscrollcommand=vertical.set)
        self.tree.config(xscrollcommand=horizontal.set)
        vertical.config(command=self.tree.yview)
        horizontal.config(command=self.tree.xview)

    def fixed_map(self, style, option):
        return [elm for elm in style.map("Treeview", query_opt=option)
                if elm[:2] != ("!disabled", "!selected")]

    def __update_item(self):
        pass

    def __delete_item(self):
        pass

    def openLinkItem(self):
        LinkItemFile = filedialog.askopenfilename(filetypes=[("DumpAttach", ".json")],defaultextension=".json")
        if "/" in LinkItemFile:
            LinkItemFile = LinkItemFile.split("/")[-1]       
        self.__loadLinkItem(LinkItemFile)



    def __loadLinkItem(self,LinkItemFile):
        self.database.session.query(Bullets).delete()
        self.database.session.query(Magazines).delete()
        self.database.session.query(Attachments).delete()
        self.database.session.query(LinkBulletMag).delete()
        self.database.session.query(LinkBullets).delete()
        self.database.session.query(LinkMags).delete()
        self.database.session.query(LinkAttachments).delete()
        
        self.database.session.commit()    

        with open(LinkItemFile, 'r') as myfile:
            data=myfile.read()
        attachments = json.loads(data)["HlyngeWeapons"]

        for item in attachments:
            item_name = item.get("name")
            for attach in item.get("attachments"):
                exists = self.database.session.query(Attachments).filter_by(name=attach).first()
                if not exists:
                    item_obj = Attachments(name = attach)
                    self.database.session.add(item_obj)
                
                exists = self.database.session.query(LinkAttachments).filter_by(attachname=attach, itemname=item_name).first()
                if not exists:
                    item_obj = LinkAttachments(attachname=attach, itemname=item_name)
                    self.database.session.add(item_obj)
        
            for mag in item.get("magazines"):
                exists = self.database.session.query(Magazines).filter_by(name=mag).first()
                if not exists:
                    #Mag_MKII_10Rnd
                    x=0
                    if "rnd" in mag.lower():
                        x = mag.lower().split("rnd")[-2].split("_")[-1]
                        x = re.sub("[^0-9]", "", x)
                    item_obj = Magazines(name = mag,magbulletcount = int(x))
                    self.database.session.add(item_obj)
                exists = self.database.session.query(LinkMags).filter_by(magname=mag, itemname=item_name).first()
                if not exists:
                    item_obj = LinkMags(magname=mag, itemname=item_name)
                    self.database.session.add(item_obj)

            for bullet in item.get("bullets"):
                exists = self.database.session.query(Bullets).filter_by(name=bullet).first()
                if not exists:
                    item_obj = Bullets(name = bullet)
                    self.database.session.add(item_obj)
                
                exists = self.database.session.query(LinkBullets).filter_by(bulletname=bullet, itemname=item_name).first()
                if not exists:
                    item_obj = LinkBullets(bulletname=bullet, itemname=item_name)
                    self.database.session.add(item_obj)
                    
                for mag in item.get("magazines"):
                    exists = self.database.session.query(LinkBulletMag).filter_by(bulletname=bullet, magname=mag).first()
                    if not exists:
                        item_obj = LinkBulletMag(bulletname=bullet, magname=mag)
                        self.database.session.add(item_obj)
        self.database.session.commit()

def testWindow():
    window = Tk()
    LinkItem(window)
    window.mainloop()
