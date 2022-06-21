import telebot
from telebot import types
from db import *
import psycopg2
# -*- coding: utf-8 -*-
"""
My modules.
"""
from Mytoken import token

""""""""""""
API_TOKEN = token
bot = telebot.TeleBot(API_TOKEN)


# START BOT
class Start:
    @bot.message_handler(func=lambda message: message.text == "↖ На Главную")
    @bot.message_handler(commands=['start'])
    def menu(message):
        chat_id = message.chat.id
        first_buttons = types.ReplyKeyboardMarkup(
            row_width=2, resize_keyboard=True)
        btn1 = types.KeyboardButton("Категории")
        btn2 = types.KeyboardButton("ТОП 10 лучших товаров")
        first_buttons.add(btn1, btn2)
        bot.reply_to(message, text=f"""Здравствуйте {message.from_user.first_name}!
        Вас приветствует Телеграм БОТ. Добро пожаловать в наших Магазин\n\n
        Пожалуйста выберите, что нибудь из предолженного и следуйте дальше по инструкции
""", reply_markup=first_buttons)


# CATEGORY DATA
DATA_CATEGORY = {}
PRODUCT_CHOICES = (
    ("wardrobes", "⭐ ШКАФ"),
    ("bedroom-sets", "⭐ СПАЛЬНИ"),
    ("hallways", "⭐ ПРИХОЖИЕ"),
    ("kitchens", "⭐ КУХНИ"),
    ("tv-stand", "⭐ TV ТУМБЫ"),
    ("dressers", "⭐ КОМОДЫ"),
    ("living-room-sets", "⭐ ГОСТИНЫЕ"),
    ("children-sets", "⭐ ДЕТСКИЕ & ОФИС"),
    ("cushioned-furniture", "⭐ МЯГКАЯ МЕБЕЛЬ"),
)
for item in PRODUCT_CHOICES:
    DATA_CATEGORY[item[1]] = item[0]


class Product:
    # CATEGORY CODE
    @bot.message_handler(func=lambda message: message.text == "Категории" or message.text == "◀ Назад в категории")
    def category(message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn1 = types.KeyboardButton("↖ На Главную")
        row = [types.KeyboardButton(x) for x in DATA_CATEGORY.keys()]
        row.append(btn1)
        markup.add(*row)
        categories = []
        for k, v in DATA_CATEGORY.items():
            categories.append(f'{v}. {k}')
        x = '\n'.join(categories)
        m = bot.send_message(
            chat_id, text=f"Выберите Категорию ⬇⬇⬇", reply_markup=markup)

    # PRODUCT VIEW
    @bot.message_handler(func=lambda message: message.text in [x for x in DATA_CATEGORY.keys()])
    def product(message):
        chat_id = message.chat.id
        if message.text != "◀ Назад в категории" or message.text != "↖ На Главную":
            global DATA_PRODUCT
            DATA_PRODUCT= {}
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT * FROM product_product where type='{DATA_CATEGORY[message.text]}'"
            )
            data = cursor.fetchall()
            for item in data:
                DATA_PRODUCT[item[1]] = item[0]
            chat_id = message.chat.id
            markup = types.InlineKeyboardMarkup(row_width=2)
            row = [types.InlineKeyboardButton(f"📋 {k}", callback_data=f"{v}") for k, v in DATA_PRODUCT.items()]
            markup.add(*row)
            m = bot.send_message(chat_id, text=f"Выберите Продукт:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def product_detail(call):
        bot.answer_callback_query(call.id)
        chat_id = call.message.chat.id
        if int(call.data) in [x for x in DATA_PRODUCT.values()]:
            cursor = connection.cursor()
            cursor.execute(
                f'SELECT * FROM product_product where product_product.id = {int(call.data)}'
            )
            data = cursor.fetchall()
            DATA_PRODUCT_DETAIL = {}
            product_link = f"http://127.0.0.1:8000/product/{int(call.data)}/"
            products = []

            for item in data:
                type = {v: k for k, v in DATA_CATEGORY.items()}
                try:
                    products.append(f' ID: {item[0]}\n ИМЯ: "{item[1]}"\n ОПИСАНИЕ: "{item[2]}"\n ЦЕНА : "{item[3]}"\n '
                                    f'Категория: "{type.get(item[4])}"\n ДАТА ДОБАВЛЕНИЯ: "{item[7]}"\n '
                                    f'Производитель: "{item[5]}"\n Фото: "{item[9]}"')
                except:
                    products.append(f' ID: {item[0]}\n ИМЯ: {item[1]}\n ОПИСАНИЕ: {item[2]}\n ЦЕНА :'
                                    f' {item[3]}\n Категория: "{type.get(item[4])}"\n ДАТА ДОБАВЛЕНИЯ: {item[7]}\n '
                                    f'Производитель: {item[5]}\n Фото: ""')
                x = '\n'.join(products)
                log_title = [item[1] for item in data]
                log_title = '\n'.join(log_title)
                m = bot.send_message(chat_id,
                                     text=f'<b>{log_title}</b><pre>{x}</pre> \n\nLink: <b>{product_link}</b>',
                                     parse_mode='HTML')
        else:
            m = bot.send_message(
                chat_id, text=f"Продукты такого типа не найдена попробуйте другие")
bot.infinity_polling()
