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
    def __init__(self, name, location = None, phone=None):
        self.name = name
        self.location = location
        self.phone = phone

      

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == "private":
        name = message.from_user.first_name
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        button_info = types.KeyboardButton(text="ℹ️ Ma'lumot olish")
        button_book = types.KeyboardButton(text="🛒 Buyurtma qilish")
        keyboard.add(button_book,button_info)
        bot.reply_to(message, name + " Kerakli bo'limni tanlang",parse_mode= "Markdown", reply_markup=keyboard)
        
@bot.message_handler(content_types=['text'])
def userRequest(message):
    if message.chat.type == "private":
        if message.text == "ℹ️ Ma'lumot olish":
            bot.send_message(message.chat.id, info_text)
            start(message)
        elif message.text == "🛒 Buyurtma qilish": 
            bot.send_message(message.chat.id, "Ism-Familyangizni yozing")
            bot.register_next_step_handler(message, process_name_step)
        else:
            bot.send_message(message.chat.id, "Bunday bo'lim mavjud emas")
            start(message)
      
def process_name_step(message):
    if message.text == '/start':
        userRequest(message)
    else:
        try:
            global userName
            chat_id = message.chat.id
            name = message.text
            userName = name
            user = User(name)
            user_dict[chat_id] = user
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_phone = types.KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
            keyboard.add(button_phone)
            bot.send_message(message.chat.id, "Telefon raqamingizni yuboring", reply_markup=keyboard)
            bot.register_next_step_handler(message, process_phone_step)
        
        except Exception as e:
            bot.reply_to(message, "Xatolik mavjud. Iltimos, qaytadan kiriting")
        
def process_phone_step(message):
    try:
        chat_id = message.chat.id
        if message.content_type != 'contact' or message.text == '/start':
            bot.reply_to(message, 'Xatolik mavjud. Iltimos, qaytadan kiriting')
            bot.register_next_step_handler(message, process_phone_step)
        user = user_dict[chat_id]
        user.phone = message.text
        phone = User(user.phone)
        if message.content_type == 'contact':
            global phone_num
            phone_num = message.contact.phone_number
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
            region1 = types.InlineKeyboardButton(text="Toshkent")
            region2 = types.InlineKeyboardButton(text="Andijon")
            region3 = types.InlineKeyboardButton(text="Farg'ona")
            region3 = types.InlineKeyboardButton(text="Namangan")
            region4 = types.InlineKeyboardButton(text="Sirdaryo")
            region5 = types.InlineKeyboardButton(text="Jizzax")
            region6 = types.InlineKeyboardButton(text="Qashqadaryo")
            region7 = types.InlineKeyboardButton(text="Xorazm")
            region8 = types.InlineKeyboardButton(text="Buxoro")
            region9 = types.InlineKeyboardButton(text="Surhondaryo")
            region10 = types.InlineKeyboardButton(text="Urganch")
            region11 = types.InlineKeyboardButton(text="Navoiy")    
            region12 = types.InlineKeyboardButton(text="Samarqand")
            region13 = types.InlineKeyboardButton(text="Qoraqalpog'iston")
            markup.add(region1,region2,region3,region4,region5,region6,region7,region8,region9,region10,region11,region12,region13)
            bot.send_message(message.chat.id, "Qaysi viloyatdansiz ?", reply_markup=markup)
            bot.register_next_step_handler(message, process_location_step)
    except Exception as e:
        bot.reply_to(message, "Xatolik mavjud. Iltimos, qaytadan kiriting")

def process_location_step(message):
    global province
    province = message
    try:
        kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        confirm = types.KeyboardButton(text="Ha")
        reject = types.KeyboardButton(text="Yo'q")
        kb.add(confirm, reject)
        bot.send_message(message.chat.id, "Joylashuvingizni jo'natishni hohlaysizmi ?", reply_markup=kb)
        bot.register_next_step_handler(message, process_userChoice_step)
    except Exception as e:
        bot.send_message(message.chat.id, e)

def process_userChoice_step(message):
    try:
        if message.text == "Ha":
            kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
            sendLocation = types.KeyboardButton(text="Joylashuvni jo'natish", request_location=True)
            kb.add(sendLocation)
            bot.reply_to(message, "Joylashuvingizni jo'nating", reply_markup=kb)
            bot.register_next_step_handler(message, process_userLocation_step)
        elif message.text == "Yo'q":
            process_region_step(province)
            global ul
            ul = "jo'natishni hoxlamadi"
        else:
            bot.send_message(message, "Mavjud bo'lmagan buyruq.")
            bot.register_next_step_handler(message, process_userChoice_step)
            
    except Exception as e:
        bot.send_message(message.chat.id, "Xatolik mavjud. Iltimos, qaytadan kiriting")

def process_userLocation_step(message):
    if message.content_type == 'location':
        try:
            chat_id = message.chat.id
            location = message.text
            process_region_step(province)
            global latitude, longitude, ul
            latitude = message.location.latitude
            longitude = message.location.longitude
            ul = "https://www.google.com/search?q=%s,%s"%(latitude,longitude)
            print(ul)
        except Exception as e:
            bot.send_message(message.chat.id, "Xatolik mavjud. Iltimos, qaytadan kiriting")
    else:   
        bot.send_message(message.chat.id, "Xatolik mavjud. Iltimos, qaytadan kiriting")
        time.sleep(1)
        process_location_step(province)

def process_region_step(message):
    try:
        chat_id = message.chat.id
        if message.content_type != 'text':
            bot.reply_to(message, 'Xatolik mavjud. Iltimos, qaytadan kiriting')
            bot.register_next_step_handler(message, process_phone_step)
        user = user_dict[chat_id]
        user.location = message.text
        location = User(user.location)
        if message.content_type == 'text':
            global userRegion
            userRegion = message.text
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
            confirm = types.InlineKeyboardButton(text="Tasdiqlash")
            reject = types.InlineKeyboardButton(text="Bekor qilish")
            markup.add(confirm, reject)
            bot.send_message(message.chat.id, "Kiritilgan ma'lumotlaringiz tog'riligini tekshiring" + "\nIsmingiz: "
                             + user.name + "\nViloyat: "+userRegion+"\nTelefon: "
                             + phone_num +"\nMa'lumotlarni tasdiqlaysizmi ?", 
                             reply_markup=markup)
            bot.register_next_step_handler(message, process_confirm_step)
    except Exception as e:
        bot.reply_to(message, "Xatolik mavjud. Iltimos, qaytadan kiriting")
        
def process_confirm_step(message):
    chat_id = message.chat.id
    confirm = message.text
    user = user_dict[chat_id]
    if (confirm == u'Tasdiqlash'):
        user.confirm = confirm
        bot.send_message(message.chat.id, 'Rahmat, siz bilan imkon qadar tezroq aloqaga chiqamiz.')
        bot.send_message(-1001508537723, '#Mijoz\n' + "Ismi: " + user.name + "\nUsername: @"
                         +message.from_user.username+"\nViloyati: #"
                         +userRegion+"\nTelefon raqami: "
                         + phone_num +"\nManzil "+ul)
        time.sleep(1)
        start(message)
    else:   
        user_dict.clear()
        msg = bot.send_message(message.chat.id, 'Bekor qilindi,\nIsm-Familyangizni qaytadan kiriting')
        bot.register_next_step_handler(message, process_name_step)

bot.enable_save_next_step_handlers()

bot.load_next_step_handlers()

# bot.polling()
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://dashboard.heroku.com/apps/alhikmauz") # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.  
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)