import threading
import time
import telegram
import telegram.ext


class BotTele:
    def __init__(self, token, user_id, private):
        self.TOKEN = token
        self.USER_ID = user_id
        self.PRIVATE = private

        self.application = telegram.ext.ApplicationBuilder().token(self.TOKEN).build()

        self.start_handler = telegram.ext.CommandHandler("start", self.__start)
        self.stop_handler = telegram.ext.CommandHandler("stop", self.__stop)

        self.application.add_handler(self.start_handler)
        self.application.add_handler(self.stop_handler)

    threads = {}
    time_checker_name = "time_checker"

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

    def __time_checker(self, signal):
        return

    def __test_work_imitation(self, signal):
        name = threading.current_thread().name
        counter = 0
        while not signal.is_set():
            print(counter)
            counter += 1
            time.sleep(5)

        self.threads.clear()
        print("Received StopSignal, ending ", name)

    @staticmethod
    def __stop_thr(signal):
        if signal.is_set():
            print("Nothing to stop")
            return

        print("Trying to stop")
        try:
            signal.set()
        except KeyError:
            pass

    async def __start(self, update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
        if self.PRIVATE:
            if str(update.effective_user.id) == self.USER_ID:
                print(len(self.threads))
                if len(self.threads) == 0:
                    time_checker_event = threading.Event()
                    time_checker_thread = threading.Thread(target=self.__time_checker,
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
