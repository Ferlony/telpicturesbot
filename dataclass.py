from dataclasses import dataclass
from os import sep
import configparser
from config_class import ConfigClass


@dataclass
class BotTeleData(ConfigClass):
    def __init__(self):
        self.__CONFIG_PATH = "local" + sep + "config.ini"
        config = configparser.ConfigParser()
        config.read(self.__CONFIG_PATH)

        self.TOKEN = config["SECRETS"]["TOKEN"]
        self.USER_ID = config["SECRETS"]["USER_ID"]
        self.CHAT_ID = config["SECRETS"]["CHAT_ID"]
        self.PRIVATE = bool(config["DEFAULT"]["PRIVATE"])
        self.PICTURE_LOCATION_DEFAULT = config["DEFAULT"]["picture_location_default"]
        self.SLEEP_TIME = int(config["DEFAULT"]["sleep_time"])
        ConfigClass.__init__(self, self.__CONFIG_PATH, "INDEXES")
