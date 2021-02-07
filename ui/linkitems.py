from tkinter import Tk, Toplevel, Frame, StringVar, Radiobutton, Label, Entry, Button, filedialog,OptionMenu
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



Base = declarative_base()

class LinkItem(object):

    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.grab_set()
        self.config = ConfigManager("config.xml")
        self.database = Dao(self.config.get_database())
        self.configFrame = Frame(self.window)
        self.configFrame.grid(row=3, column=0, sticky="n,w,e", padx=30)

        Label(self.configFrame, text="Select the LinkItems File:").grid(row=1, column=0, sticky="w")
# Buttons
        Button(
            self.configFrame, text="Open", width=12, command=self.openLinkItem
        ).grid(row=2, column=0, sticky="w", padx=25)
        self.window.wait_window()


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
