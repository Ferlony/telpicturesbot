import threading
import time
import telegram
import telegram.ext
import signal
import os
import asyncio
from datetime import datetime
import depfuns


class BotTele:
    def __init__(self, token, user_id, chat_id, private, picture_location_default=None, picture_index=0):
        self.__TOKEN = token
        self.__USER_ID = user_id
        self.__CHAT_ID = chat_id
        self.__PRIVATE = private
        self.__PICTURE_LOCATION_DEFAULT = picture_location_default

        self.__picture_index = picture_index
        self.__files_list, self.__files_list_amount = depfuns.get_files_in_dir(self.__PICTURE_LOCATION_DEFAULT)

    __threads = {}

    __time_checker_name = "time_checker"
    __started_without_polling_flag = False

    @property
    def files_in_dir(self):
        return self.__files_list

    @property
    def files_in_dir_amount(self):
        return self.__files_list_amount

    @property
    def picture_index_current(self):
        return self.__picture_index

    @property
    def files_types_in_dir(self):
        return depfuns.get_file_types_in_list(self.__files_list)

    @property
    def picture_location(self):
        return self.__PICTURE_LOCATION_DEFAULT

    @picture_location.setter
    def picture_location(self, new_picture_location):
        self.__PICTURE_LOCATION_DEFAULT = new_picture_location

    def start_polling(self):
        if self.__started_without_polling_flag:
            print("Bot has been started without polling\nTo start with polling turn it off")
        else:
            application = telegram.ext.ApplicationBuilder().token(self.__TOKEN).build()

            start_handler = telegram.ext.CommandHandler("start", self.__start)
            stop_handler = telegram.ext.CommandHandler("stop", self.__stop)
            kill_handler = telegram.ext.CommandHandler("kill", self.__kill)
            update_files_handler = telegram.ext.CommandHandler("update", self.__update)
            get_info_handler = telegram.ext.CommandHandler("info", self.__info)

            application.add_handler(start_handler)
            application.add_handler(stop_handler)
            application.add_handler(kill_handler)
            application.add_handler(update_files_handler)
            application.add_handler(get_info_handler)

            application.run_polling()

    def start_without_polling(self):
        if len(self.__threads) == 0:
            time_checker_event = threading.Event()
            time_checker_thread = threading.Thread(target=self.__test_work_imitation,
                                                   name=self.__time_checker_name,
                                                   args=[time_checker_event],
                                                   daemon=False)

            self.__threads[self.__time_checker_name] = (time_checker_event, time_checker_thread)

            for ev, thr in self.__threads.values():
                if not thr.is_alive():
                    thr.start()

            self.__started_without_polling_flag = True
            print("Bot started without polling")
        else:
            print("Bot has already been started without polling")

    # TODO async?
    def stop_without_polling(self):
        if len(self.__threads) > 0:
            self.__stop_thr(self.__threads[self.__time_checker_name][0])
            self.__started_without_polling_flag = False
            print("Bot without polling has ended")
        else:
            print("Bot without polling has not been started")

    async def get_bot_info(self):
        bot = telegram.Bot(self.__TOKEN)
        async with bot:
            return await bot.get_me()

    async def get_update_info(self):
        bot = telegram.Bot(self.__TOKEN)
        async with bot:
            return await bot.get_updates()

    async def send_message_to_chat_id(self, message):
        bot = telegram.Bot(self.__TOKEN)
        async with bot:
            return await bot.send_message(text=message, chat_id=self.__CHAT_ID)

    # TODO
    async def send_file_to_chat_id(self, file_location=None):
        bot = telegram.Bot(self.__TOKEN)
        if file_location:
            depfuns.file_checker()



        return

    def update_files_list(self):
        now_files_list_amount = self.__files_list_amount
        self.__files_list, self.__files_list_amount = depfuns.get_files_in_dir(self.__PICTURE_LOCATION_DEFAULT)
        return self.__files_list_amount - now_files_list_amount

    def __time_checker(self, event_signal: threading.Event):  # TODO: change time into file
        name = threading.current_thread().name
        while not event_signal.is_set():
            time_now = datetime.now().strftime("%H")
            if time_now == "00" or time_now == "02" \
                    or time_now == "04" or time_now == "06" \
                    or time_now == "08" or time_now == "10" \
                    or time_now == "12" or time_now == "14" \
                    or time_now == "16" or time_now == "18" \
                    or time_now == "20" or time_now == "22":
                asyncio.run(self.send_file_to_chat_id())

        self.__threads.clear()
        print("Received StopSignal, ending ", name)

    def __test_work_imitation(self, event_signal: threading.Event):
        name = threading.current_thread().name
        counter = 0
        while not event_signal.is_set():
            print(counter)
            counter += 1
            time.sleep(5)

        self.__threads.clear()
        print("Received StopSignal, ending ", name)

    @staticmethod
    def __stop_thr(event_signal: threading.Event):
        if event_signal.is_set():
            print("Nothing to stop")
            return

        print("Trying to stop")
        try:
            event_signal.set()
        except KeyError:
            pass

    async def __start(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.__PRIVATE:
            if str(update.effective_user.id) == self.__USER_ID:
                print(len(self.__threads))
                if len(self.__threads) == 0:
                    time_checker_event = threading.Event()
                    time_checker_thread = threading.Thread(target=self.__test_work_imitation,
                                                           name=self.__time_checker_name,
                                                           args=[time_checker_event],
                                                           daemon=False)

                    self.__threads[self.__time_checker_name] = (time_checker_event, time_checker_thread)

                    for ev, thr in self.__threads.values():
                        if not thr.is_alive():
                            thr.start()
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text="Bot has started")
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text="Bot has already been started")

    async def __stop(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.__PRIVATE:
            if str(update.effective_user.id) == self.__USER_ID:
                if len(self.__threads) > 0:
                    self.__stop_thr(self.__threads[self.__time_checker_name][0])
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text="Bot has ended")
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text="Bot has not been started")

    async def __kill(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.__PRIVATE:
            if str(update.effective_user.id) == self.__USER_ID:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="Killing bot")
                os.kill(os.getpid(), signal.SIGINT)

    async def __update(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.__PRIVATE:
            if str(update.effective_user.id) == self.__USER_ID:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=str(self.update_files_list()))

    async def __info(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.__PRIVATE:
            if str(update.effective_user.id) == self.__USER_ID:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=(str(self.picture_index_current) + "/" +
                                                     str(self.files_in_dir_amount) + "\n" +
                                                     str(self.files_types_in_dir)))
