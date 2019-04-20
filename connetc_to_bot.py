#!/usr/bin/python

from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import logging

TOKEN='818241522:AAHxrav_2d0yH4ATeHnyRQMYnYM9uxtDyxo'
REQUEST_KWARGS={
    'proxy_url': 'http://142.93.34.45:3128/'
}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()