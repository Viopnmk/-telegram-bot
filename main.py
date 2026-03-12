import telebot

from config import TOKEN
from market import btc_price,eth_price
from analysis import btc_analysis
from strategy import strategy
from multitf import multi_tf
from levels import levels

bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])

def start(message):

    bot.reply_to(message,"量化机器人启动成功 🤖")


@bot.message_handler(commands=['btc'])

def btc(message):

    p=btc_price()

    bot.reply_to(message,f"BTC价格: ${p}")


@bot.message_handler(commands=['eth'])

def eth(message):

    p=eth_price()

    bot.reply_to(message,f"ETH价格: ${p}")


@bot.message_handler(commands=['analysis'])

def analysis(message):

    bot.reply_to(message,btc_analysis())


@bot.message_handler(commands=['strategy'])

def strat(message):

    bot.reply_to(message,strategy())


@bot.message_handler(commands=['multitf'])

def mt(message):

    bot.reply_to(message,multi_tf())


@bot.message_handler(commands=['levels'])

def lv(message):

    bot.reply_to(message,levels())


bot.polling()