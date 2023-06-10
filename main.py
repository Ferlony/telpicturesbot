import logging
import menus
import bot_tele


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    try:
        menus.Menu(bot_tele.BotTele()).main_menu()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
