#!/usr/bin/env python3

import sys
import logging
import config
import telebot
import queue
from imp import reload

reload(sys)

bot = telebot.TeleBot(config.tgtoken)
last_start_time = None

logging_mode = logging.INFO
log = logging.getLogger('bot')
log.setLevel(logging_mode)
fh = logging.FileHandler('bot.log')
fh.setLevel(logging_mode)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(threadName)19s][%(module)12s][%(levelname)8s] %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
log.addHandler(fh)
log.addHandler(ch)

q = queue.Queue()
