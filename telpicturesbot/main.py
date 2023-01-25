import configparser
from os import sep
import logging
import menus
import bot_tele


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    config = configparser.ConfigParser()
    config.read("local" + sep + "config.ini")
    TOKEN = config["SECRETS"]["TOKEN"]
    USER_ID = config["SECRETS"]["USER_ID"]
    CHAT_ID = config["SECRETS"]["CHAT_ID"]
    PRIVATE = bool(config["DEFAULT"]["PRIVATE"])
    PICTURE_LOCATION_DEFAULT = "local" + sep + "pictures" + sep + config["DEFAULT"]["picture_location_default"]
    PICTURE_INDEX = int(config["DEFAULT"]["PICTURE_INDEX"])

    try:
        menus.Menu(bot_tele.BotTele(TOKEN, USER_ID, CHAT_ID, PRIVATE, PICTURE_LOCATION_DEFAULT, PICTURE_INDEX)).main_menu()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
