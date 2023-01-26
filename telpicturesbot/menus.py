from bot_tele import BotTele
from depfuns import conformation
import asyncio


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
                  "'6' Send message to chat id\n"
                  "'7' Send file to chat id\n"
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
                message = input("Input message")
                print(asyncio.run(self.bot_tele.send_message_to_chat_id(message)))
            elif inp == "7":
                file = input("Input absolute file location")
                if conformation():
                    self.bot_tele.send_file_to_chat_id(file)
            elif inp == "8":
                pass  # TODO: edit config menu and json creator
            elif inp == "0":
                print("Closing program")
                break
            else:
                print("Wrong input")

    def __get_info_menu(self):
        while True:
            print("'1' Get bot info\n"
                  "'2' Get user update info\n"
                  "'3' Get files in dir and their status\n"
                  "'4' Get files in dir extensions\n"
                  "'0' Back")
            inp = input()
            if inp == "1":
                print(asyncio.run(self.bot_tele.get_bot_info()))
            elif inp == "2":
                print(asyncio.run(self.bot_tele.get_update_info()))  # Should send message to the bot
            elif inp == "3":
                print("Files in dir:\n", self.bot_tele.files_list)
                print("Files status:\n", str(self.bot_tele.pictures_index) + "/" +
                      str(self.bot_tele.files_list_amount))
            elif inp == "4":
                print("Files extensions:\n", self.bot_tele.files_types_in_list)
            elif inp == "0":
                print("Back")
                break
            else:
                print("Wrong input")
