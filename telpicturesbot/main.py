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
    bot_polling_started_flag = False
    while True:
        print("Choose action\n"
              "'1' Start bot polling\n"
              "'2' Get bot info\n"
              "'3' Get user update info\n"
              "'4' Send message to user\n"
              "'0' Close program")
        inp = input()
        if inp == "1":
            bot_tele.start_polling()
        elif inp == "3":
            print(asyncio.run(bot_tele.get_bot_info()))
        elif inp == "4":
            print(asyncio.run(bot_tele.get_update_info()))  # Should send message to the bot
        elif inp == "5":
            message = input("Input message")
            print(asyncio.run(bot_tele.send_message_to_chat_id(message)))
        elif inp == "0":
            print("Closing program")
            break
        else:
            print("Wrong input")


def main():
    config = configparser.ConfigParser()
    config.read("local" + sep + "config.ini")
    TOKEN = config["SECRETS"]["TOKEN"]
    USER_ID = config["SECRETS"]["USER_ID"]
    CHAT_ID = config["SECRETS"]["CHAT_ID"]
    PRIVATE = bool(config["DEFAULT"]["PRIVATE"])

    menus(BotTele.BotTele(TOKEN, USER_ID, CHAT_ID, PRIVATE))


if __name__ == "__main__":
    main()
