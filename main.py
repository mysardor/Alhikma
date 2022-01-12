
import telebot
from telebot import types
import sys
from typing import Text
from flask import Flask
from telebot.util import user_link
sys.dont_write_bytecode = True
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()
import telebot
from telebot import types
from settings import *
from info import *
import time
from flask import Flask, request
import logging

bot = telebot.TeleBot(BOT_TOKEN)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def start(message):
    if message.chat.type == "private":
        msg = bot.reply_to(message, """Исм/Фамилия:""")
        bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    if message.chat.type == "private":
        try:
            chat_id = message.chat.id
            global name
            name = message.text
            user = User(name)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, """Компаниянгиз номи:""")
            bot.register_next_step_handler(msg, process_company_step)
        except Exception as e:
            bot.reply_to(message, 'oooops, кутилмаган қарор!')


def process_company_step(message):
    if message.chat.type == "private":
        try:
            chat_id = message.chat.id
            global company
            company = message.text
            user = User(company)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, """Лавозимингиз (агар ходим бўлсангиз):""")
            bot.register_next_step_handler(msg, process_job_step)
        except Exception as e:
            bot.reply_to(message, 'oooops, кутилмаган қарор!')

def process_job_step(message):
    if message.chat.type == "private":
        try:
            chat_id = message.chat.id
            global job
            job = message.text
            user = User(job)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, """Компаниянгизнинг ўртача ойлик пул айланмаси (ихтиёрий):""")
            bot.register_next_step_handler(msg, process_money_step)
        except Exception as e:
            bot.reply_to(message, 'oooops, кутилмаган қарор!')

def process_money_step(message):
    if message.chat.type == "private":
        try:
            chat_id = message.chat.id
            global money
            money = message.text
            user = User(money)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, """Бизнесингизда қандай муаммолар учрамоқда:""")
            bot.register_next_step_handler(msg, process_problem_step)
        except Exception as e:
            bot.reply_to(message, 'oooops, кутилмаган қарор!')

def process_problem_step(message):
    if message.chat.type == "private":
        try:
            chat_id = message.chat.id
            global problem
            problem = message.text
            user = User(problem)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, """Бугунги тадбирдан кутувларингиз:""")
            bot.register_next_step_handler(msg, process_wait_step)
        except Exception as e:
            bot.reply_to(message, 'oooops, кутилмаган қарор!')

def process_wait_step(message):
    if message.chat.type == "private":
        try:
            chat_id = message.chat.id
            global waitin
            waitin = message.text
            user = User(waitin)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, """Спикерга саволларингиз:""")
            bot.register_next_step_handler(msg, process_question_step)
        except Exception as e:
            bot.reply_to(message, 'oooops, кутилмаган қарор!')

def process_question_step(message):
    if message.chat.type == "private":
        try:
            chat_id = message.chat.id
            global question
            question = message.text
            user = User(question)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, """Сиз билан бўгланишимиз учун телефон рақамингизни қолдиринг.""")
            bot.register_next_step_handler(msg, process_phone_step)
        except Exception as e:
            bot.reply_to(message, 'oooops, кутилмаган қарор!')

def process_phone_step(message):
    if message.chat.type == "private":
        try:
            chat_id = message.chat.id
            global phoneNum
            phoneNum = message.text
            user = User(question)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, """Ёзган маълумотларингиз тўгрилигини текширинг""")
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
            confirm = types.InlineKeyboardButton(text="Тасдиқлаш")
            reject = types.InlineKeyboardButton(text="Қайта бошлаш")
            markup.add(confirm, reject)
            chat_id = message.chat.id
            bot.send_message(chat_id, 'Исм-Фамилянгиз: ' + name + '\n Компаниянгиз номи: ' + company + '\n Лавозимингиз: ' + job + '\n Ойлик айланмангиз: ' + money + 
            '\n Муаммоларингиз: ' + problem  + '\n Тадбирдан кутаётганингиз: ' + waitin  + '\n Телефон рақамингиз: ' + phoneNum , 
            reply_markup=markup)
            bot.register_next_step_handler(msg, process_confirm_step)
        except Exception as e:
            bot.reply_to(message, 'oooops, кутилмаган қарор!')

def process_confirm_step(message):
    try:
        chat_id = message.chat.id
        confirm = message.text
        user = user_dict[chat_id]
        if (confirm == u'Тасдиқлаш'):
            user.confirm = confirm
            bot.send_message(message.chat.id, 'Раҳмат, сиз билан имкон қадар тезроқ алоқага чиқамиз.')
            bot.send_message(-1001595060544,'Исм-Фамилянгиз: ' + name + '\n Компаниянгиз номи: ' + company + '\n Лавозимингиз: ' + job + '\n Ойлик айланмангиз: ' + money + 
        '\n Муаммоларингиз: ' + problem  + '\n Тадбирдан кутаётганингиз: ' + waitin  + '\n Телефон рақамингиз: ' + phoneNum)
            # time.sleep(1)
            # start(message)
        else:   
            user_dict.clear()
            msg = bot.send_message(message.chat.id, 'Бекор қилинди,\nИсм-Фамилянгизни қайтадан киритинг')
            bot.register_next_step_handler(message, process_name_step)

        
    except Exception as e:
        bot.reply_to(message, 'oooops, кутилмаган қарор!')


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.infinity_polling()