import configparser


class INIManager(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.config = configparser.ConfigParser()

    def write_ini(self, section, sub_section, value):
        self.config[section] = {}
        self.config[section][sub_section] = str(value)
        with open(self.file_name, 'w') as configfile:
            self.config.write(configfile)

    def read_ini(self, section, sub_section):
        self.config.read(self.file_name)
        return self.config[section][sub_section]
