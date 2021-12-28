import xml.etree.ElementTree as ET
from model.item import Item
from config import ConfigManager


def is_mag(name):
    if "mag" in name.lower():
        return True
    else:
        return False


def is_ammo(name):
    if "ammo" in name.lower():
        return True
    else:
        return False


def is_optics(name):
    name = name.lower()
    if "optic" in name or "lrs" in name:
        return True
    else:
        return False


class XMLReader(object):
    def __init__(self, filename):

        with open(filename) as file:
            lines = file.readlines()
        print(''.join(lines))
        self.parser = XMLParser(''.join(lines))

    def _get_parser(self):
        return self.parser


class XMLParser(object):
    def __init__(self, string_data):
        self.string_data = string_data
        self.xml = ET.fromstring(self.string_data)
        self.mod_prefixes = ["Mass", "GP_", "gp_", "FP4_"]
        self.config = ConfigManager("config.xml")
        self.not_gun_keywords = [
            "lrs",
            "ammo",
            "optic",
            "sawed",
            "suppressor",
            "goggles",
            "mag",
            "light",
            "rnd",
            "bayonet",
            "railatt",
            "compensator",
            "drum",
            "palm",
            "STANAG",
            "buttstock",
            "bttstck",
            "handguard",
            "hndgrd",
        ]

    def get_items(self, mapname):
        items = list()
        usage_name = "usage" if mapname == "Normal Map" else "tag"
        tier_attrib = "name" if mapname == "Normal Map" else "user"
        for item_value in self.xml.iter("type"):
            item = Item()
            usages = list()
            tiers = list()
            item.name = item_value.attrib["name"]
            if item_value.find('category') is None:
                item.cat_type = 'object'
            for i in item_value:
                if i.tag == "nominal":
                    item.nominal = i.text
                elif i.tag == "restock":
                    item.restock = i.text
                elif i.tag == "min":
                    item.min = i.text
                elif i.tag == "quantmin":
                    item.qmin = i.text
                elif i.tag == "quantmax":
                    item.qmax = i.text
                elif i.tag == "category":
                    item.cat_type = i.attrib["name"]
                elif i.tag == "lifetime":
                    item.lifetime = i.text.strip()
                elif i.tag == usage_name:
                    try:
                        usages.append(i.attrib["name"])
                    except:
                        pass
                elif i.tag == "value":
                    try:
                        tiers.append(i.attrib[tier_attrib])
                    except KeyError:
                        pass
                elif i.tag == "flags":
                    item.dynamic_event = i.attrib["deloot"]
                    item.count_in_hoarder = i.attrib["count_in_hoarder"]
                    item.count_in_cargo = i.attrib["count_in_cargo"]
                    item.count_in_player = i.attrib["count_in_player"]
                    item.count_in_map = i.attrib["count_in_map"]

            item.usage = ",".join(usages)
            item.tier = ",".join(tiers)
            items.append(item)
        return items

    def __get_type(self, name):
        if self.__is_gun(name=name):
            return "gun"
        if is_ammo(name=name):
            return "ammo"
        if is_mag(name=name):
            return "mag"
        if is_optics(name=name):
            return "optic"
        return "attachment"

    def __is_gun(self, name):
        is_gun = True
        name = self.__remove_mod_prefix(name=name)
        for keyword in self.not_gun_keywords:
            if keyword in name.lower():
                is_gun = False
                break
        return is_gun

    def __remove_mod_prefix(self, name):
        for prefix in self.mod_prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]
        return name
