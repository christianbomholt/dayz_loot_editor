from tkinter import Tk, Toplevel, Frame, StringVar, Radiobutton, Label, Entry, Button, filedialog, OptionMenu, IntVar
from tkinter import ttk, VERTICAL, HORIZONTAL, LabelFrame,Tcl
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, and_, func
from sqlalchemy.orm import sessionmaker, mapper
from model.item import Item, init_database, Base
from model.item import Mapselect,Attachments,LinkAttachments,LinkBulletMag,LinkBullets,LinkMags,Magazines,Bullets
from config import ConfigManager
from database.dao import Dao
from sqlalchemy.ext.declarative import declarative_base
import json
import re
from utility import attach_definition


#Base = declarative_base()

class LinkItem(object):

    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.grab_set()
        self.config = ConfigManager("config.xml")
        self.database = Dao(self.config.get_database())
        self.searchName = StringVar()
        self.gridAttachs = []
        self.__create_entry_frame()
        self.__create_tree_view()
        self.table = f'{self.attach.get()}'
        self.__initiate_attachs()
        self.tree.bind("<ButtonRelease-1>", self.__fill_entry_frame)


    def __create_entry_frame(self):
        self.entryFrameHolder = Frame(self.window)
        self.entryFrameHolder.grid(row=0, column=0, sticky="nw")
        self.entryFrame = Frame(self.entryFrameHolder)
        self.entryFrame.grid(padx=8, pady=6)
        optionList = ('attachments', 'bullets', 'magazines')
        self.attach = StringVar()
        self.attach.set(optionList[0])
        OptionMenu(self.entryFrame, self.attach, *optionList, command = self.__setattach__
        ).grid(row=0, column=0, sticky="n,s,e,w",columnspan=2)

        # labels
        Label(self.entryFrame, text="Name").grid(row=1, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Count").grid(row=2, column=0, sticky="w", pady=5)
        Label(self.entryFrame, text="Prop").grid(row=3, column=0, sticky="w", pady=5)

        # input variables
        self.id = IntVar()
        self.name = StringVar()
        self.attachcount = IntVar()
        self.prop = IntVar()
        
        # form fields
        self.nameField = Entry(self.entryFrame, textvariable=self.name)
        self.nameField.grid(row=1, column=1, sticky="w")
        self.countField = Entry(self.entryFrame, textvariable=self.attachcount)
        self.countField.grid(row=2, column=1, sticky="w")
        self.propField = Entry(self.entryFrame, textvariable=self.prop)
        self.propField.grid(row=3, column=1, sticky="w")

        Button(
            self.entryFrame, text="Update", width=8, command=self.__update_attach
        ).grid(row=4, column=0, pady=5, sticky="e")

        Button(
            self.entryFrame, text="Delete", width=8, command=self.__delete_attach
        ).grid(row=4, column=1, pady=5, sticky="w")

        # Search frame
        self.searchFrame = Frame(self.entryFrameHolder,borderwidth="2", relief="ridge")
        self.searchFrame.grid(row=2, column=0, sticky="n,w,e", padx=30)
        Label(self.searchFrame, text="Search like name:").grid(row=1, column=0, sticky="n")

        self.serchName = Entry(self.searchFrame, textvariable=self.searchName, width=14).grid(row=2, columnspan=2, pady=5, padx=10, sticky="nesw")
        Button(
            self.searchFrame, text="Search", width=12, command=self.__search_attach_name__
        ).grid(row=3, column=0, sticky="w", padx=5,pady=10)
        Button(
            self.searchFrame, text="Reset", width=12, command=self.__initiate_attachs
        ).grid(row=3, column=1, sticky="e", padx=5,pady=10)

        # Load Config files frame
        self.configFrame = Frame(self.entryFrameHolder,borderwidth="2", relief="ridge")
        self.configFrame.grid(row=3, column=0, sticky="n,w,e", padx=30)
        Label(self.configFrame, text="Select the LinkAttach File:").grid(row=1, column=0, sticky="n")

        Button(
            self.configFrame, text="Open", width=12, command=self.openLinkItem
        ).grid(row=2, column=0, sticky="s", padx=30,pady=10)


    def __search_attach_name__(self):
            if self.searchName.get() != "":
                attachs = self.database.search_attach_name(self.get_class_by_tablename(self.table),self.searchName.get())
                self.__populate_attachs(attachs)
                self.gridAttachs = attachs
                self.searchName.set("") 

    def get_class_by_tablename(self,tablename):
        for c in Base._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
                return c

    def __setattach__(self,selection):
        self.table = f'{self.attach.get()}'
        self.__initiate_attachs()
        

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

    def __update_attach(self):
        def __update_helper(attach, field, default_value):
            value_from_update_form = getattr(self, field).get()
            if value_from_update_form != default_value:
                setattr(attach, field, value_from_update_form)

        for attachs in self.treeView.selection():
            attach = self.treeView.item(attachs)
            id_of_interest = attach["text"]
            attach_to_update = self.database.session.query(self.get_class_by_tablename(self.table)).get(id_of_interest)
            __update_helper(attach_to_update, "attachcount", -1)
            __update_helper(attach_to_update, "prop", -1)
            self.database.session.commit()
        self.__populate_attachs(self.gridAttachs)

    def __delete_attach(self):
        for attachs in self.treeView.selection():
            attach = self.treeView.item(attachs)
            itemid = attach["text"]
            self.database.delete_attach(self.get_class_by_tablename(self.table),itemid)
        self.__populate_attachs(self.gridAttachs)


    def __initiate_attachs(self, attachs=None):
        attachs = self.database.session.query(self.get_class_by_tablename(self.table))
        self.gridAttachs = attachs
        self.__populate_attachs(attachs.all())
        self.searchName.set("") 

    def __populate_attachs(self, attachs):
        if self.tree.get_children() != ():
            self.tree.delete(*self.tree.get_children())
        for idx,i in enumerate(attachs): 
            if idx % 2 == 0:
                self.tree.insert("", "end", text=i.id, value=[i.name,i.attachcount,i.prop],tags=('evenrow',))
            else:
                self.tree.insert("", "end", text=i.id, value=[i.name,i.attachcount,i.prop],tags=('oddrow',))
        self.tree.tag_configure('oddrow', background='#FFFFFF')
        self.tree.tag_configure('evenrow', background='#F5F5F5')

    def __fill_entry_frame(self, event):        
        tree_row = self.tree.item(self.tree.focus())
        id = tree_row["text"]
        attach = self.database.get_attach(self.get_class_by_tablename(self.table),id)
        if attach:
            self.id.set(id)
            self.name.set(attach.name)
            self.attachcount.set(-1)
            self.prop.set(-1)

    def tree_view_sort_column(self,tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_view_sort_column(tv, col, not reverse)) 

    def openLinkItem(self):
        LinkItemFile = filedialog.askopenfilename(filetypes=[("DumpAttach", ".json")],defaultextension=".json")
        if "/" in LinkItemFile:
            LinkItemFile = LinkItemFile.split("/")[-1]       
        self.__loadLinkItem(LinkItemFile)



    def __loadLinkItem(self,LinkItemFile):
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
                    x=0
                    if "rnd" in mag.lower():
                        x = mag.lower().split("rnd")[-2].split("_")[-1]
                        x = re.sub("[^0-9]", "", x)
                    item_obj = Magazines(name = mag,attachcount = int(x))
                    self.database.session.add(item_obj)
                exists = self.database.session.query(LinkMags).filter_by(magname=mag, itemname=item_name).first()
                if not exists:
                    item_obj = LinkMags(magname=mag, itemname=item_name)
                    self.database.session.add(item_obj)

            for bullet in item.get("bullets"):
                exists = self.database.session.query(Bullets).filter_by(name = bullet).first()
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
