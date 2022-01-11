from xml.dom import minidom
import xml.etree.ElementTree as ET
import os


class ConfigManager(object):
    def __init__(self, config_file):
        self.cofig_name = config_file
        print(os.getcwd())
        self.config_file = minidom.parse(config_file)

    def get_usages(self):
        usage_list = self.config_file.getElementsByTagName("usage")
        usages = list()
        for i in usage_list:
            usages.append(i.attributes["value"].value)
        usages.append("None")
        return usages

    def get_database(self):
        database = self.config_file.getElementsByTagName("database")
        return database[0].attributes["value"].value

    def get_mapselect(self):
        mapselect = self.config_file.getElementsByTagName("mapselect")
        return mapselect[0].attributes["value"].value

    def get_cat_types(self):
        cat_type_list = self.config_file.getElementsByTagName("category")
        cat_types = list()
        for i in cat_type_list:
            cat_types.append(i.attributes["value"].value)
        return cat_types

    def get_types(self):
        type_list = self.config_file.getElementsByTagName("type")
        types = list()
        for i in type_list:
            types.append(i.attributes["value"].value)
        return types

    def get_sub_types(self):
        type_list = self.config_file.getElementsByTagName("sub_type")
        types = list()
        for i in type_list:
            types.append(i.attributes["value"].value)
        return types

    def get_tiers(self):
        tier_list = self.config_file.getElementsByTagName("tier")
        tiers = list()
        for i in tier_list:
            tiers.append(i.attributes["value"].value)
        tiers.append("None")
        return tiers

    def get_import_mod(self):
        mod_list = self.config_file.getElementsByTagName("import_mod")
        import_mods = list()
        for i in mod_list:
            import_mods.append(i.attributes["value"].value)
        return import_mods

    def get_hive(self):
        hive_list = self.config_file.getElementsByTagName("hive")
        hive = list()
        for i in hive_list:
            hive.append(i.attributes["value"].value)
        return hive

    def get_traders(self):
        trader_list = self.config_file.getElementsByTagName("trader")
        traders = list()
        for i in trader_list:
            traders.append(i.attributes["value"].value)
        traders.append("EXCLUDE")
        return traders

    def get_rarities(self):
        rarity_list = self.config_file.getElementsByTagName("rarity")
        rarities = list()
        for i in rarity_list:
            rarities.append(i.attributes["value"].value)
        return rarities

    def get_tree_heading(self):
        column_list = self.config_file.getElementsByTagName("node")
        columns_info = list()
        columns = list()
        for i in column_list:
            columns_info.append(
                [
                    i.attributes["text"].value,
                    i.attributes["width"].value,
                    i.attributes["col_id"].value,
                    i.attributes["stretch"].value,
                ]
            )
            columns.append(i.attributes["text"].value)
        return columns, columns_info

    def set_database(self, name):
        tree = ET.parse(self.cofig_name)
        # root = tree.getroot()
        elems = tree.findall('databasefile')
        for elem in elems:
            list(elem)[0].set("value", name)
        tree.write(self.cofig_name)
