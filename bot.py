from datetime import datetime, timedelta
from Commands.functions import *
from DBconnect.config import *
from Config.config import *
from PIL import Image, ImageDraw, ImageFont
import telebot
from telebot import types
import requests
import datetime
import schedule
import threading
import time
import re
import os
import mysql.connector

cwd = os.getcwd()

post_list = []
mycursor = mydb.cursor()


@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda message: message.text == 'Привет')
def send_welcome(message):
    username = get_username(message)
    chat_id = str(message.chat.id)
    if(user_exist(chat_id) == False):
        put_user(chat_id,username)

    markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=False)
    itembtn1 = types.KeyboardButton('Настроить Автопостинг')
    markup.add(itembtn1)
    bot.send_message(message.chat.id, "Команды:", reply_markup=markup)

def process_groupname_step(message):
    try:
        name = str((message.text)).replace('@','')
        number = bot_is_in_group(name)
        if number == 0:
            text = 'Вы не добавили бота в администраторы вашей группы/канала.\nДобавьте бота в чат/канал/группу и назначьте\nнеобходимые права.'
            bot.send_message(str(message.chat.id), text = text)
        elif number == 1 or number == 2:
            post_list.append(name)
            msg = bot.reply_to(message, 'Выберите время для публикации в канале и введите в четком формате без пробелов.\nНапример: 17:00')
            if(group_exist(name) == False):
                put_group(str(message.chat.id), name)

                bot.register_next_step_handler(msg, process_time_step)

            elif number == 3:
                text = 'Вы добавили бота в администраторы вашего канала.\nНо не выдали необходимых прав.\nПерейдите в настроки администаторов канала и\nи разрешите боту постить сообщения'
                bot.send_message(message.chat.id, text = text)

    except Exception as e:
        bot.reply_to(message, 'Такого чата не существует, нажмите добавить еще раз и введите верный username чата/канала/группы')
        msg = bot.reply_to(message, "Введите username вашего канала.")
        bot.register_next_step_handler(msg, process_groupname_step)

def process_time_step(message):
    try:
        splitmessage = message.text.split()
        if(len(splitmessage)>1):
            text = 'Введите время в правильном формате!'
            bot.send_message(message.chat.id, text = text)
            msg = bot.reply_to(message, 'Выберите время для публикации и введите в четком формате без пробелов.\nНапример: 17:00')
            bot.register_next_step_handler(msg, process_time_step)
        else:
            if(validate_time(str(message.text))):
                put_post(user_list[0], str(message.text))
                text = 'Отлично в назначенное время ' + message.text + ' пост придет в Ваш канал'
                bot.send_message(message.chat.id, text = text)
            else:
                text = 'Введите время в правильном формате!'
                bot.send_message(message.chat.id, text = text)
                msg = bot.reply_to(message, 'Выберите время для публикации и введите в четком формате без пробелов.\nНапример: 17:00')
                bot.register_next_step_handler(msg, process_time_step)

    except Exception as e:
        bot.reply_to(message, 'Введите время в правильном формате!')
        msg = bot.reply_to(message, 'Выберите время для публикации и введите в четком формате без пробелов.\nНапример: 17:00')
        bot.register_next_step_handler(msg, process_time_step)


@bot.message_handler(content_types=['text'])
def settings(message):
    mtext = message.text
    if(mtext == 'Настроить Автопостинг'):
        markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=False)
        itembtn1 = types.KeyboardButton('Добавить группу и пост')
        markup.add(itembtn1)
        bot.send_message(message.chat.id, "Команды:", reply_markup=markup)
    elif(mtext == 'Добавить группу и пост'):
        msg = bot.reply_to(message, "Введите username вашего канала.")
        bot.register_next_step_handler(msg, process_groupname_step)




bot.polling(none_stop=True, interval=0)
