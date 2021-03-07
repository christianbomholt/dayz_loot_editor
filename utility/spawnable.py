from tkinter import Tk, filedialog,OptionMenu
from model.item import Item,LinkBulletMag,LinkBullets,LinkMags,Magazines,Bullets
import xml.etree.cElementTree as ET


def exportSpawnable(session, items):
    fname  = filedialog.asksaveasfilename(filetypes=[("xml file", ".xml")],defaultextension=".xml")
    if fname is not None:
        weapons = items.filter(Item.item_type=="ranged")
        root = ET.Element("type")
        for weapon in weapons:
            print("DEBUG exportSpawnable  :", weapon.name)
            attachment = get_class(session,"attachments",weapon.name)
            mags = get_class(session,"magazines",weapon.name)
            weapon_sub = ET.SubElement(root,"type", name = weapon.name)
            write_subelement(root, attachments)
            write_subelement(root, bullets)
            write_subelement(root, mags)

        tree = ET.ElementTree(root)
        tree.write(fname)

def write_subelement(root, item_list):
    attach_sub = ET.SubElement(root, "attachments")
    for item in item_list:
        ET.SubElement(attach_sub, "item", name=item.name, chance=str(item.prop))

def get_class_by_tablename(tablename):
    for c in Base._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c 

def get_class(session, tablename, name):
    class_ = get_class_by_tablename(tablename)
    return session.query(
            class_
        ).filter(
             Item.name == name,
        ).filter(
            Item.name == LinkMags.itemname
        ).filter(
            LinkMags.magname == Magazines.name
        ).filter(
            Item.name == LinkBullets.itemname
        ).filter(
            LinkBullets.bulletname == Bullets.name
        ).filter(
            Item.name == LinkAttachments.itemname
        ).filter(
            LinkAttachments.attachname == Attachments.name
        ).filter(
            class_.prop>0
        ).all()