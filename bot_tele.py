import threading
import time
import telegram
import telegram.ext
import signal
import os
import asyncio
import depfuns
from dataclass import BotTeleData
from datetime import datetime


class BotTele(BotTeleData):
    def __init__(self):
        BotTeleData.__init__(self)
        self.__pictures_index = int(self.get_key_value_in_config(self.PICTURE_LOCATION_DEFAULT))
        self.__files_list, self.__files_list_amount = depfuns.get_files_in_dir(self.PICTURE_LOCATION_DEFAULT)
        self.__sleep_sending_time = self.SLEEP_TIME

    __threads = {}

    __time_checker_name = "time_checker"
    __started_without_polling_flag = False

    __time_checker_sleep_error = 30

    @property
    def files_list(self):
        return self.__files_list

    @property
    def files_list_amount(self):
        return self.__files_list_amount

    @property
    def files_types_in_list(self):
        return depfuns.get_file_types_in_list(self.__files_list)

    @property
    def pictures_index(self):
        return int(self.__pictures_index)

    @pictures_index.setter
    def pictures_index(self, value):
        self.set_key_value_in_config(self.PICTURE_LOCATION_DEFAULT, value)
        self.__pictures_index = self.read_key_from_config(self.PICTURE_LOCATION_DEFAULT)

    @property
    def sleep_sending_time(self):
        return self.__sleep_sending_time

    @sleep_sending_time.setter
    def sleep_sending_time(self, value):
        self.__sleep_sending_time = int(value)

    @property
    def picture_location(self):
        return self.PICTURE_LOCATION_DEFAULT

    @picture_location.setter
    def picture_location(self, new_picture_location):
        self.PICTURE_LOCATION_DEFAULT = new_picture_location
        self.__pictures_index = int(self.get_key_value_in_config(self.PICTURE_LOCATION_DEFAULT))
        self.update_files_list()

    def start_polling(self):
        if self.__started_without_polling_flag:
            print("Bot has been started without polling\nTo start with polling turn it off")
        else:
            application = telegram.ext.ApplicationBuilder().token(self.TOKEN).build()

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
            time_checker_thread = threading.Thread(target=self.__time_checker,
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

    def stop_without_polling(self):
        if len(self.__threads) > 0:
            self.__stop_thr(self.__threads[self.__time_checker_name][0])
            self.__started_without_polling_flag = False
            print("Bot without polling has ended")
        else:
            print("Bot without polling has not been started")

    async def get_bot_info(self):
        bot = telegram.Bot(self.TOKEN)
        async with bot:
            return await bot.get_me()

    async def get_update_info(self):
        bot = telegram.Bot(self.TOKEN)
        async with bot:
            return await bot.get_updates()

    async def send_message_to_chat_id(self, message):
        bot = telegram.Bot(self.TOKEN)
        async with bot:
            return await bot.send_message(text=message, chat_id=self.CHAT_ID)

    async def send_file_to_chat_id(self, file_location=None):
        bot = telegram.Bot(self.TOKEN)
        file_to_send_renamed, file_type = self.__rename_file_and_check_file_type(file_location)

        if file_type == "picture":
            async with bot:
                await bot.send_photo(photo=file_to_send_renamed, chat_id=self.CHAT_ID)
            if file_location:
                print("Picture ", file_location, " sent renamed")
            else:
                print("Picture ", self.__files_list[self.pictures_index], " sent renamed")
        elif file_type == "animation":
            async with bot:
                await bot.send_animation(animation=file_to_send_renamed, chat_id=self.CHAT_ID)
            if file_location:
                print("Animation ", file_location, " sent renamed")
            else:
                print("Animation ", self.__files_list[self.pictures_index], " sent renamed")
        elif file_type == "video":
            async with bot:
                await bot.send_video(video=file_to_send_renamed, chat_id=self.CHAT_ID)
            if file_location:
                print("Video ", file_location, " sent renamed")
            else:
                print("Video ", self.__files_list[self.pictures_index], " sent renamed")
        else:
            async with bot:
                await bot.send_message(text=("Could not send " + self.__files_list[self.pictures_index]),
                                       chat_id=self.USER_ID)
            print("Could not send ", self.__files_list[self.pictures_index])

        if file_location:
            return
        else:
            if file_type:
                if self.pictures_index < self.files_list_amount - 1:
                    now_picture_index = self.pictures_index + 1
                    self.pictures_index = now_picture_index
                else:
                    self.pictures_index = 0

    def __rename_file_and_check_file_type(self, file_location):
        if file_location:
            file_type = depfuns.file_checker(file_location)
            if file_type:
                return depfuns.rename_one_file_by_hash_one(file_location), file_type
        else:
            file_type = depfuns.file_checker(self.files_list[self.pictures_index])
            if file_type:
                return depfuns.rename_one_file_by_hash(self.picture_location, self.files_list[self.pictures_index]), \
                    file_type

    def update_files_list(self):
        now_files_list_amount = self.__files_list_amount
        self.__files_list, self.__files_list_amount = depfuns.get_files_in_dir(self.PICTURE_LOCATION_DEFAULT)
        return self.__files_list_amount - now_files_list_amount

    def __time_checker(self, event_signal: threading.Event):
        name = threading.current_thread().name
        while not event_signal.is_set():
            while not event_signal.is_set():
                try:
                    asyncio.run(self.send_file_to_chat_id())
                    break
                except Exception as e:
                    print(e)
                    time.sleep(self.__time_checker_sleep_error)
            time.sleep(self.sleep_sending_time)

        print("Received StopSignal, ending ", name)

    def start_without_polling_in_bg(self):
        while True:
            #while True:
            start_time = datetime.now().timestamp()
            try:
                asyncio.run(self.send_file_to_chat_id())
            except Exception as e:
                print(e)
                #time.sleep(self.__time_checker_sleep_error)
            execution_time = datetime.now().timestamp() - start_time
            time.sleep(float(self.sleep_sending_time) - execution_time)

    def __stop_thr(self, event_signal: threading.Event):
        if event_signal.is_set():
            print("Nothing to stop")
            return

        print("Trying to stop")
        try:
            event_signal.set()
            self.__threads.clear()
        except KeyError:
            pass

    async def __start(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.PRIVATE:
            if str(update.effective_user.id) == self.USER_ID:
                print(len(self.__threads))
                if len(self.__threads) == 0:
                    time_checker_event = threading.Event()
                    time_checker_thread = threading.Thread(target=self.__time_checker,
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
        if self.PRIVATE:
            if str(update.effective_user.id) == self.USER_ID:
                if len(self.__threads) > 0:
                    self.__stop_thr(self.__threads[self.__time_checker_name][0])
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text="Bot has ended")
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text="Bot has not been started")

    async def __kill(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.PRIVATE:
            if str(update.effective_user.id) == self.USER_ID:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="Killing bot")
                os.kill(os.getpid(), signal.SIGINT)

    async def __update(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.PRIVATE:
            if str(update.effective_user.id) == self.USER_ID:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=str(self.update_files_list()))

    async def __info(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.PRIVATE:
            if str(update.effective_user.id) == self.USER_ID:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=(str(self.__pictures_index + 1) + "/" +
                                                     str(self.__files_list_amount) + "\n" +
                                                     str(self.files_types_in_list)))
