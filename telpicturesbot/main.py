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
    CONFIG_PATH = "local" + sep + "config.ini"
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    TOKEN = config["SECRETS"]["TOKEN"]
    USER_ID = config["SECRETS"]["USER_ID"]
    CHAT_ID = config["SECRETS"]["CHAT_ID"]
    PRIVATE = bool(config["DEFAULT"]["PRIVATE"])
    PICTURE_LOCATION_DEFAULT = config["DEFAULT"]["picture_location_default"]
    SLEEP_TIME = int(config["DEFAULT"]["sleep_time"])

    try:
        menus.Menu(bot_tele.BotTele(TOKEN, USER_ID,
                                    CHAT_ID, PRIVATE,
                                    CONFIG_PATH, PICTURE_LOCATION_DEFAULT, SLEEP_TIME)).main_menu()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
