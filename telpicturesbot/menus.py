import asyncio
import signal
import os
from bot_tele import BotTele
from depfuns import conformation
from config_class import ConfigClass


class Menu:
    def __init__(self, bot_tele: BotTele):
        self.bot_tele = bot_tele

    def main_menu(self):
        while True:
            print("Choose action\n"
                  "'1' Start bot polling\n"
                  "'2' Start bot without polling\n"
                  "'3' Stop bot without polling\n"
                  "'4' Update files in dir\n"
                  "'5' Get info menu\n"
                  "'6' Send menu\n"
                  "'7' Set bot menu\n"
                  "'8' Edit config\n"
                  "'0' Close program")
            inp = input()
            if inp == "1":
                self.bot_tele.start_polling()
            elif inp == "2":
                self.bot_tele.start_without_polling()
            elif inp == "3":
                self.bot_tele.stop_without_polling()
            elif inp == "4":
                difference = self.bot_tele.update_files_list()
                if difference >= 0:
                    print("Added ", difference, " new files")
                else:
                    print("Removed ", difference, " files")
            elif inp == "5":
                self.__get_info_menu()
            elif inp == "6":
                self.__send_menu()
            elif inp == "7":
                self.__set_bot_menu()
            elif inp == "8":
                self.__config_menu()
            elif inp == "0":
                print("Closing program")
                os.kill(os.getpid(), signal.SIGKILL)
            else:
                print("Wrong input")

    def __get_info_menu(self):
        while True:
            print("'1' Get bot info\n"
                  "'2' Get user update info\n"
                  "'3' Get files in dir status\n"
                  "'4' Get files in dir extensions\n"
                  "'0' Back")
            inp = input()
            if inp == "1":
                print(asyncio.run(self.bot_tele.get_bot_info()))
            elif inp == "2":
                print(asyncio.run(self.bot_tele.get_update_info()))  # Should send message to the bot
            elif inp == "3":
                # print("Files in dir:\n", self.bot_tele.files_list)
                print("Files status:\n", str(self.bot_tele.pictures_index + 1) + "/" +
                      str(self.bot_tele.files_list_amount))
            elif inp == "4":
                print("Files extensions:\n", self.bot_tele.files_types_in_list)
            elif inp == "0":
                print("Back")
                break
            else:
                print("Wrong input")

    def __config_menu(self):
        config_path = self.bot_tele.config_path
        # config_path = "local" + sep + "test_config.ini"
        while True:
            print("'1' Create config\n"
                  "'2' Set value for key\n"
                  "'0' Back")
            inp = input()
            if inp == "1":
                try:
                    ConfigClass(config_path, None).create_config()
                except Exception as e:
                    print(e)
            elif inp == "2":
                try:
                    while True:
                        print("Choose Key:\n"
                              "'1' picture_location_default\n"
                              "'2' sleep time\n"
                              "'3' chat_id\n"
                              "'4' user_id\n"
                              "'5' token\n"
                              "'0' Back")
                        new_inp = input()
                        if new_inp == "1":
                            print("Enter file location")
                            new_file_location = input()
                            if conformation():
                                ConfigClass(config_path, "DEFAULT").edit_value_by_key("picture_location_default",
                                                                                      new_file_location)
                        elif new_inp == "2":
                            print("Enter sleep time")
                            new_sleep_time = input()
                            if conformation():
                                ConfigClass(config_path, "DEFAULT").edit_value_by_key("sleep_time",
                                                                                      new_sleep_time)
                        elif new_inp == "3":
                            print("Enter chat_id")
                            new_chat_id = input()
                            if conformation():
                                ConfigClass(config_path, "SECRETS").edit_value_by_key("chat_id",
                                                                                      new_chat_id)
                        elif new_inp == "4":
                            print("Enter user_id")
                            new_user_id = input()
                            if conformation():
                                ConfigClass(config_path, "SECRETS").edit_value_by_key("user_id",
                                                                                      new_user_id)
                        elif new_inp == "5":
                            print("Enter token")
                            new_token = input()
                            if conformation():
                                ConfigClass(config_path, "SECRETS").edit_value_by_key("token",
                                                                                      new_token)
                        elif new_inp == "0":
                            break
                        else:
                            print("Wrong input")
                except Exception as e:
                    print(e)
            elif inp == "0":
                break
            else:
                print("Wrong input")

    def __send_menu(self):
        while True:
            print("'1' Send message to chat id\n"
                  "'2' Send file to chat id\n"
                  "'0' Back")
            inp = input()
            if inp == "1":
                print("Input message")
                message = input()
                if conformation():
                    print(asyncio.run(self.bot_tele.send_message_to_chat_id(message)))
            elif inp == "2":
                print("Input absolute file location")
                file = input()
                if conformation():
                    print(asyncio.run(self.bot_tele.send_file_to_chat_id(file)))
            elif inp == "0":
                break
            else:
                print("Wrong input")

    def __set_bot_menu(self):
        while True:
            print("'1' Set bot new file location\n"
                  "'2' Set bot file index\n"
                  "'3' Set bot sleep time"
                  "'0' Back")
            inp = input()
            if inp == "1":
                print("Enter new file location")
                new_picture_location = input()
                if conformation():
                    self.bot_tele.picture_location = new_picture_location
            elif inp == "2":
                print("Enter file index")
                file_index = int(input())
                if conformation():
                    self.bot_tele.pictures_index = file_index
            elif inp == "3":
                print("Enter new sleep time")
                new_sleep_time = int(input())
                if conformation():
                    self.bot_tele.sleep_sending_time = new_sleep_time
            elif inp == "0":
                break
            else:
                print("Wrong input")
