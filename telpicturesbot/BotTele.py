import threading
import time
import telegram
import telegram.ext
import signal
import os
from datetime import datetime


class BotTele:
    def __init__(self, token, user_id, chat_id, private):
        self.TOKEN = token
        self.USER_ID = user_id
        self.CHAT_ID = chat_id
        self.PRIVATE = private

        self.application = telegram.ext.ApplicationBuilder().token(self.TOKEN).build()

        self.start_handler = telegram.ext.CommandHandler("start", self.__start)
        self.stop_handler = telegram.ext.CommandHandler("stop", self.__stop)
        self.kill_handler = telegram.ext.CommandHandler("kill", self.__kill)

        self.application.add_handler(self.start_handler)
        self.application.add_handler(self.stop_handler)
        self.application.add_handler(self.kill_handler)

    threads = {}
    time_checker_name = "time_checker"

    picture_sender_flag = False

    def start_polling(self):
        self.application.run_polling()

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
            try:
                await bot.send_message(text=message, chat_id=self.CHAT_ID)
                return 0
            except Exception as e:
                print(e)
                return -1

    async def send_picture_to_chat_id(self):
        return

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
                self.picture_sender_flag = True

        self.threads.clear()
        print("Received StopSignal, ending ", name)

    def __test_work_imitation(self, event_signal: threading.Event):
        name = threading.current_thread().name
        counter = 0
        while not event_signal.is_set():
            print(counter)
            counter += 1
            time.sleep(15)

        self.threads.clear()
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
        if self.PRIVATE:
            if str(update.effective_user.id) == self.USER_ID:
                print(len(self.threads))
                if len(self.threads) == 0:
                    time_checker_event = threading.Event()
                    time_checker_thread = threading.Thread(target=self.__test_work_imitation,
                                                           name=self.time_checker_name,
                                                           args=[time_checker_event],
                                                           daemon=False)

                    self.threads[self.time_checker_name] = (time_checker_event, time_checker_thread)

                    for ev, thr in self.threads.values():
                        if not thr.is_alive():
                            thr.start()
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot has started")
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text="Bot has already been started")

    async def __stop(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.PRIVATE:
            if str(update.effective_user.id) == self.USER_ID:
                if len(self.threads) > 0:
                    self.__stop_thr(self.threads[self.time_checker_name][0])
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot has ended")
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot has not been started")

    async def __kill(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.PRIVATE:
            if str(update.effective_user.id) == self.USER_ID:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Killing bot")
                os.kill(os.getpid(), signal.SIGINT)
