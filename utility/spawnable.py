from tkinter import Tk, filedialog,OptionMenu
from model.item import Base, Item, LinkBulletMag, LinkBullets, LinkAttachments, LinkMags, Attachments, Magazines, Bullets
import xml.etree.cElementTree as ET


def exportSpawnable(session, items):
    fname  = filedialog.asksaveasfilename(filetypes=[("xml file", ".xml")],defaultextension=".xml")
    if fname is not None:
        weapons = items.filter(Item.item_type=="ranged")
        root = ET.Element("type")
        for weapon in weapons:
            if weapon.nominal > 0:
                tagtype = ET.SubElement(root,"type",name=weapon.name)
                tagattach = get_class(session,"attachments",weapon.name)
                tagmags = get_class(session,"magazines",weapon.name)
                write_subelement(root,"attachments", tagattach)
                write_subelement(root,"mags", tagmags)

        prettify(root)
        tree = ET.ElementTree(root)
        tree.write(fname)

def write_subelement(root,tag, item_list):
    attach_sub = ET.SubElement(root, tag)

    for item in item_list:
        if item is None:
            ET.SubElement(attach_sub, "item", name=item.name, chance=str(item.prop))

def get_class_by_tablename(tablename):
    for c in Base._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c 

def get_class(session, tablename, name):
    class_ = get_class_by_tablename(tablename)
    result = session.query(
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
    i = len(result)
    if i > 0:
        print("DEBUG result :", result)
        return result

def prettify(element, indent='  '):
    queue = [(0, element)]  # (level, element)
    while queue:
        level, element = queue.pop(0)
        children = [(level + 1, child) for child in list(element)]
        if children:
            element.text = '\n' + indent * (level+1)  # for child open
        if queue:
            element.tail = '\n' + indent * queue[0][0]  # for sibling open
        else:
            element.tail = '\n' + indent * (level-1)  # for parent close
        queue[0:0] = children  # prepend so children come before siblings        