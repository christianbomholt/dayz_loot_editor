from xml.dom import minidom


class ConfigManager(object):
    def __init__(self, config_file):
        self.config_file = minidom.parse(config_file)

    def get_usages(self):
        usage_list = self.config_file.getElementsByTagName("usage")
        usages = list()
        for i in usage_list:
            usages.append(i.attributes["value"].value)
        return usages

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
        return tiers

    def get_mods(self):
        mod_list = self.config_file.getElementsByTagName("mod")
        mods = list()
        for i in mod_list:
            mods.append(i.attributes["value"].value)
        return mods

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
