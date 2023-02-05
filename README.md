# telpicturesbot

About
=====

Telegram bot which allows to send different files and messages to chat id. It also can send them with some time interval.

Installation
============
```
git clone https://github.com/Ferlony/telpicturesbot
cd telpicturesbot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Edit config.ini located in telpicturesbot/local/ by setting your telegram bot token got from @BotFather, your user id and chat id where you want to post, set sleep_time in seconds, awaiting time before next post and picture_location_default, files that will be sent to chat id

Example located in test_config.ini

Usage
=====
```
python main.py
```
