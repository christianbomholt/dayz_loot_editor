import xml.etree.ElementTree as ET
from model.item import Item


def get_type_block(item: Item):
    type_block = ET.Element('type')
    type_block.set('name', item.name)
    # nominal
    nominal = ET.SubElement(type_block, 'nominal')
    nominal.text = str(item.nominal)
    # restock
    restock = ET.SubElement(type_block, 'restock')
    restock.text = str(item.restock)
    # lifetime
    lifetime = ET.SubElement(type_block, "lifetime")
    lifetime.text = str(item.lifetime)
    # min
    _min = ET.SubElement(type_block, "min")
    _min.text = str(item.min)
    quant_min = ET.SubElement(type_block, "quantmin")
    quant_min.text = "-1"
    quant_max = ET.SubElement(type_block, "quantmax")
    quant_max.text = "1"
    cost = ET.SubElement(type_block, "cost")
    cost.text = "100"

    flags = ET.SubElement(type_block, 'flags')
    flags.set('count_in_hoarder', str(item.count_in_hoarder))
    flags.set('count_in_player', str(item.count_in_player))
    flags.set('count_in_map', str(item.count_in_map))
    flags.set('count_in_cargo', str(item.count_in_cargo))
    flags.set('crafted', "0")
    flags.set('deloot', str(item.dynamic_event))
    category = ET.SubElement(type_block, 'category')
    category.set("name", str(item.item_type))
    #
    usages = str(item.usage)
    usages = usages.split(",")
    for i in usages:
        usage = ET.SubElement(type_block, 'usage')
        usage.set("name", i)
    tires = item.tire.split(',')

    for i in tires:
        tire = ET.SubElement(type_block, 'value')
        tire.set('name', i)

    return ET.tostring(type_block).decode("utf-8").replace("><", ">\n<")


class XMLWriter(object):
    def __init__(self, filename):
        self.filename = filename

    def export_xml(self, items):
        xml_file = open(self.filename, "a")
        xml_file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
        xml_file.write("\n<types>")
        for i in items:
            xml_file.write("\n" + get_type_block(i))
        xml_file.write("\n</types>")
