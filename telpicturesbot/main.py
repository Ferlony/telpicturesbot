import configparser
import asyncio
from os import sep
import logging
import BotTele


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def menus(bot_tele: BotTele.BotTele):
    bot_started_flag = False
    while True:
        print("Choose action\n"
              "'1' Start bot\n"
              "'2' Stop bot\n"
              "'3' Get bot info\n"
              "'4' Get user update info\n"
              "'0' Close program")
        inp = input()
        if inp == "1":
            bot_tele.start_polling()  # TODO: make multiprocess
            bot_started_flag = True
        elif inp == "2":
            if bot_started_flag:
                pass  # TODO: stop fun
            else:
                print("Bot has not been started")
        elif inp == "3":
            print(asyncio.run(bot_tele.get_bot_info()))
        elif inp == "4":
            print(asyncio.run(bot_tele.get_update_info()))  # Should send message to the bot
        elif inp == "0":
            print("Closing program")
            break
        else:
            print("Wrong input")


def main():
    config = configparser.ConfigParser()
    config.read("local" + sep + "config.ini")
    USER_ID = config["SECRETS"]["USER_ID"]
    TOKEN = config["SECRETS"]["TOKEN"]
    PRIVATE = bool(config["DEFAULT"]["PRIVATE"])

    menus(BotTele.BotTele(TOKEN, USER_ID, PRIVATE))


if __name__ == "__main__":
    main()
