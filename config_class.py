import configparser
from depfuns import get_folder_name
from os import sep


class ConfigClass:
    def __init__(self, config_path, section):
        self.__config_path = config_path
        self.__section = section

    @property
    def config_path(self):
        return self.__config_path

    @config_path.setter
    def config_path(self, config_path):
        self.__config_path = config_path

    @property
    def section(self):
        return self.__section

    @section.setter
    def section(self, section):
        self.__section = section

    def create_config(self):
        print("Enter your token")
        token = input()
        print("Enter your user id")
        user_id = input()
        print("Enter chat id")
        chat_id = input()
        print("Enter sleep time")
        sleep_time = input()
        print("Enter files location")
        file_location = input()

        file = open(self.__config_path, "w")
        file.write("[DEFAULT]\n"
                   "private = True\n"
                   "sleep_time = " + sleep_time + "\n"
                   "picture_location_default = " + file_location + "\n"
                   "\n"
                   "[SECRETS]\n"
                   "token = " + token + "\n"
                   "user_id = " + user_id + "\n"
                   "chat_id = " + chat_id + "\n"
                   "\n"
                   "[INDEXES]\n")
        file.close()
        print("Config created")

    def edit_value_by_key(self, key, value):
        config = configparser.ConfigParser()
        config.read(self.__config_path)

        try:
            if config[self.__section]:
                pass
        except KeyError:
            config.add_section(self.__section)

        try:
            if config[self.__section][key]:
                config[self.__section][key] = str(value)
        except KeyError:
            config.set(self.__section, key, str(value))

        with open(self.__config_path, "w") as config_file:
            config.write(config_file)

    def read_key_from_config(self, key):
        key = get_folder_name(key + sep).replace(sep, "") + "_index"  # TODO change it

        config = configparser.ConfigParser()
        config.read(self.__config_path)

        if config[self.__section]:
            if config[self.__section][key]:
                return config[self.__section][key]

    def set_key_value_in_config(self, key, value):
        key = get_folder_name(key + sep).replace(sep, "") + "_index"  # TODO change it

        config = configparser.ConfigParser()
        config.read(self.__config_path)

        try:
            if config[self.__section]:
                pass
        except KeyError:
            config.add_section(self.__section)

        try:
            if config[self.__section][key]:
                config[self.__section][key] = str(value)
        except KeyError:
            config.set(self.__section, key, str(value))

        with open(self.__config_path, "w") as config_file:
            config.write(config_file)

    def get_key_value_in_config(self, key):
        try:
            return self.read_key_from_config(key)
        except KeyError:
            self.set_key_value_in_config(key, "0")
            return self.read_key_from_config(key)
