import xml.etree.ElementTree as ET
from model.item import Item


def get_type_block(item: Item,mapname):
    type_block = ET.Element("type")
    type_block.set("name", item.name)
    # nominal
    nominal = ET.SubElement(type_block, "nominal")
    nominal.text = str(item.nominal)
    # restock
    restock = ET.SubElement(type_block, "restock")
    restock.text = str(item.restock)
    # lifetime
    lifetime = ET.SubElement(type_block, "lifetime")
    lifetime.text = str(item.lifetime)
    # min
    _min = ET.SubElement(type_block, "min")
    _min.text = str(item.min)
    quant_min = ET.SubElement(type_block, "quantmin")
    quant_min.text = "-1"
    #max
    quant_max = ET.SubElement(type_block, "quantmax")
    quant_max.text = "1"
    cost = ET.SubElement(type_block, "cost")
    cost.text = "100"

    flags = ET.SubElement(type_block, "flags")
    flags.set("count_in_hoarder", str(item.count_in_hoarder))
    flags.set("count_in_player", str(item.count_in_player))
    flags.set("count_in_map", str(item.count_in_map))
    flags.set("count_in_cargo", str(item.count_in_cargo))
    flags.set("crafted", "0")
    flags.set("deloot", str(item.dynamic_event))

    category = ET.SubElement(type_block, "category")
    if mapname == "Namalsk":
        if item.item_type == "ranged":
            if item.subtyp == "pistols":
                category.set("name", str("pistol"))
            else:
                category.set("name", str("rifles"))
        else:
            category.set("name", str(item.cat_type))
    else:                
        category.set("name", str(item.cat_type))
    #
    usage_name = "tag" if mapname == "Namalsk" else "usage"
    usages = str(item.usage)
    usages = usages.split(",")
    for i in usages:
        usage = ET.SubElement(type_block, usage_name)
        usage.set("name", i)


    tiers = item.tier.split(",")
    for i in tiers:
        tier = ET.SubElement(type_block, "value")
        tier.set("name", i)

    return ET.tostring(type_block).decode("utf-8").replace("><", ">\n<")


class XMLWriter(object):
    def __init__(self, filename):
        self.filename = filename
        self.mapname = ""

    def export_xml(self, items, mapname):
        xml_file = open(self.filename, "a")
        self.mapname = mapname
        xml_file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
        xml_file.write("\n<types>")
        for i in items:
            xml_file.write("\n" + get_type_block(i, mapname))
        xml_file.write("\n</types>")
