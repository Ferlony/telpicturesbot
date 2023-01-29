import threading
import time
import telegram
import telegram.ext
import signal
import os
import asyncio
import depfuns
from config_class import ConfigClass


class BotTele(ConfigClass):
    def __init__(self, token, user_id, chat_id, private, config_path, picture_location_default):
        ConfigClass.__init__(self, config_path, "INDEXES")
        self.__TOKEN = token
        self.__USER_ID = user_id
        self.__CHAT_ID = chat_id
        self.__PRIVATE = private

        self.__picture_location = picture_location_default

        self.__pictures_index = int(self.get_key_value_in_config(self.__picture_location))

        self.__files_list, self.__files_list_amount = depfuns.get_files_in_dir(self.__picture_location)

    __threads = {}

    __time_checker_name = "time_checker"
    __started_without_polling_flag = False
    __time_checker_sleep_time_s = 7000

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
        self.set_key_value_in_config(self.__picture_location, value)
        self.__pictures_index = self.read_key_from_config(self.__picture_location)

    @property
    def picture_location(self):
        return self.__picture_location

    @picture_location.setter
    def picture_location(self, new_picture_location):
        self.__picture_location = new_picture_location
        self.__pictures_index = int(self.get_key_value_in_config(self.__picture_location))
        self.update_files_list()

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

            # TODO add change default bot file location handler
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

    async def send_file_to_chat_id(self, file_location=None):
        bot = telegram.Bot(self.__TOKEN)
        file_to_send_renamed = None

        if file_location:
            file_type = depfuns.file_checker(file_location)
            if file_type:
                file_to_send_renamed = depfuns.rename_one_file_by_hash_one(file_location)
        else:
            file_type = depfuns.file_checker(self.__files_list[self.pictures_index])
            if file_type:
                file_to_send_renamed = depfuns.rename_one_file_by_hash(self.__picture_location,
                                                                       self.__files_list[self.pictures_index])

        if file_type == "picture":
            async with bot:
                await bot.send_photo(photo=file_to_send_renamed, chat_id=self.__CHAT_ID)
            if file_location:
                print("Picture ", file_location, " sent renamed")
            else:
                print("Picture ", self.__files_list[self.pictures_index], " sent renamed")
        elif file_type == "animation":
            async with bot:
                await bot.send_animation(animation=file_to_send_renamed, chat_id=self.__CHAT_ID)
            if file_location:
                print("Animation ", file_location, " sent renamed")
            else:
                print("Animation ", self.__files_list[self.pictures_index], " sent renamed")
        elif file_type == "video":
            async with bot:
                await bot.send_video(video=file_to_send_renamed, chat_id=self.__CHAT_ID)
            if file_location:
                print("Video ", file_location, " sent renamed")
            else:
                print("Video ", self.__files_list[self.pictures_index], " sent renamed")
        else:
            async with bot:
                await bot.send_message(text=("Could not send " + self.__files_list[self.pictures_index]),
                                       chat_id=self.__USER_ID)
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

    def update_files_list(self):
        now_files_list_amount = self.__files_list_amount
        self.__files_list, self.__files_list_amount = depfuns.get_files_in_dir(self.__picture_location)
        return self.__files_list_amount - now_files_list_amount

    def __time_checker(self, event_signal: threading.Event):
        name = threading.current_thread().name
        while not event_signal.is_set():
            asyncio.run(self.send_file_to_chat_id())
            time.sleep(self.__time_checker_sleep_time_s)

        print("Received StopSignal, ending ", name)

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
        if self.__PRIVATE:
            if str(update.effective_user.id) == self.__USER_ID:
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
                                               text=(str(self.__pictures_index + 1) + "/" +
                                                     str(self.__files_list_amount) + "\n" +
                                                     str(self.files_types_in_list)))
