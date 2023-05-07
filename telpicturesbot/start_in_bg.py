from bot_tele import BotTele
from os import sep
import configparser


CONFIG_PATH = "local" + sep + "config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_PATH)
TOKEN = config["SECRETS"]["TOKEN"]
USER_ID = config["SECRETS"]["USER_ID"]
CHAT_ID = config["SECRETS"]["CHAT_ID"]
PRIVATE = bool(config["DEFAULT"]["PRIVATE"])
PICTURE_LOCATION_DEFAULT = config["DEFAULT"]["picture_location_default"]
SLEEP_TIME = int(config["DEFAULT"]["sleep_time"])

bot = BotTele(TOKEN, USER_ID, CHAT_ID, PRIVATE, CONFIG_PATH, PICTURE_LOCATION_DEFAULT, SLEEP_TIME)

bot.start_without_polling_in_bg()
