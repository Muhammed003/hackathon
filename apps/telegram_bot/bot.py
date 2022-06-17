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

# class User:
#     def __init__(self):
#         self.first_name = None
#         self.last_name = None
#         self.email = None
#         self.password = None
#         self.activate_code = None
#
# user = User()


class Start:
    # Handle '/start' and '/help'
    # @bot.message_handler(commands=['help', 'start'])
    @bot.message_handler(commands=['start'])
    def menu(message):
        chat_id = message.chat.id
        first_buttons = types.ReplyKeyboardMarkup(
            row_width=2, resize_keyboard=True)
        btn1 = types.KeyboardButton("Категории")
        # btn2 = types.KeyboardButton("ТОП 10 лучших товаров")
        first_buttons.add(btn1)
        bot.reply_to(message, text=f"""Здравствуйте {message.from_user.first_name}!
Вас приветствует Телеграм БОТ. Добро пожаловать в наших Магазин\n\n
Пожалуйста выберите, что нибудь из предолженного и следуйте дальше по инструкции
""", reply_markup=first_buttons)


DATA_CATEGORY = {}
cursor = connection.cursor()
cursor.execute(
    'SELECT * FROM category_category'
)
data = cursor.fetchall()
for item in data:
    DATA_CATEGORY[item[1]] = int(item[0])

@bot.message_handler(func=lambda message: message.text == "Категории")
def category(message):

    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    row = [types.KeyboardButton(x) for x in DATA_CATEGORY.values()]
    # btn3 = types.KeyboardButton("Назад")
    btn4 = types.KeyboardButton('На Главную')
    # row.append(btn3)
    row.append(btn4)
    markup.add(*row)
    categories = []
    for k,v in DATA_CATEGORY.items():
        categories.append(f'{v}. {k}')
    x = '\n'.join(categories)
    m = bot.send_message(
        chat_id, text=f"Выберите Категорию\n\n{x }", reply_markup=markup)

#
# @bot.message_handler(func=lambda message: int(message.text) in [int(x) for x in DATA_CATEGORY.values()])
# def product(message):
#     DATA_PRODUCT= {}
#     cursor = connection.cursor()
#     cursor.execute(
#         f'SELECT * FROM product_product where product_product.category_id={int(message.text)}'
#     )
#     data = cursor.fetchall()
#     for item in data:
#         DATA_PRODUCT[item[0]] = item[1]
#     chat_id = message.chat.id
#     markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#     btn3 = types.KeyboardButton("Назад")
#     btn4 = types.KeyboardButton("На Главную")
#     row = [types.KeyboardButton(x) for x in DATA_PRODUCT.keys()]
#     row.append(btn3)
#     row.append(btn4)
#     markup.add(*row)
#     products = []
#     for k, v in DATA_PRODUCT.items():
#         products.append(f'{k}. {v}')
#     x = '\n'.join(products)
#     m = bot.send_message(
#         chat_id, text=f"Выберите продукт\n\n{x}", reply_markup=markup)
#     bot.register_next_step_handler(m, product_detail)
#

def product_detail(message):
    if message.text != 'На Главную':

        DATA_PRODUCT= {}
        cursor = connection.cursor()
        cursor.execute(
            f'SELECT * FROM product_product where product_product.id = {int(message.text)}'
        )
        data = cursor.fetchall()

        cursor.execute(
            f'SELECT * FROM product_productimage where product_productimage.id = {int(message.text)}'
        )
        data_product_image = cursor.fetchall()

        for item in data_product_image:
            product_image = "http://127.0.0.1:8000/media/"+ item[1]
        for item in data:
            DATA_PRODUCT[item[0]] = item[1]
        chat_id = message.chat.id
        product_link = f"http://127.0.0.1:8000/products/{int(message.text)}/"
        if int(message.text) in [int(x) for x in DATA_PRODUCT.keys()]:
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            row = [types.KeyboardButton(x) for x in DATA_PRODUCT.keys()]
            markup.add(*row)
            products = []
            for item in data:
                try:
                    products.append(f' id: {item[0]}\n title: {item[1]}\n description: {item[2]}\n price :'
                                    f' {item[3]}\n data created: {item[4]}\n image: {product_image}')
                except:
                    products.append(f' id: {item[0]}\n title: {item[1]}\n description: {item[2]}\n price :'
                                    f' {item[3]}\n data created: {item[4]}\n image: ""')
            x = '\n'.join(products)
            log_title = [item[1] for item in data]
            log_title = '\n'.join(log_title)
            m = bot.send_message(
                chat_id, text=f'<b>{log_title}</b><pre>{x}</pre>  <b>\n\nLink:{product_link}</b>', parse_mode='HTML')
            bot.register_next_step_handler(m, product_detail)
        else:
            m = bot.send_message(
                chat_id, text=f"Такой продукт отсутствует, пожалуйста выберите другой продукт")
            bot.register_next_step_handler(m, product_detail)
    elif message.text =='На Главную':
        chat_id = message.chat.id
        first_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Категории")
        # btn2 = types.KeyboardButton("ТОП 10 лучших товаров")
        first_buttons.add(btn1)
        bot.send_message(chat_id, "Вы перешли в главное меню", reply_markup=first_buttons)
    elif message.text == 'Назад':
        chat_id = message.chat.id
        m = bot.send_message(chat_id, text=f"Вы перешли назад")
        bot.register_next_step_handler(m, product_detail)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    # if message.text == 'Назад':
    #     chat_id = message.chat.id
    #     first_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton("Категории")
    #     btn2 = types.KeyboardButton("ТОП 10 лучших товаров")
    #     first_buttons.add(btn1, btn2)
    #     bot.send_message(chat_id, "Назад", reply_markup=first_buttons)

    if message.text == 'На Главную':
        chat_id = message.chat.id
        first_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Категории")
        # btn2 = types.KeyboardButton("ТОП 10 лучших товаров")
        first_buttons.add(btn1)
        bot.send_message(chat_id, "Вы перешли в главное меню", reply_markup=first_buttons)

    elif int(message.text) in [int(x) for x in DATA_CATEGORY.values()]:
        def product(message):
            DATA_PRODUCT = {}
            cursor = connection.cursor()
            cursor.execute(
                f'SELECT * FROM product_product where product_product.category_id={int(message.text)}'
            )
            data = cursor.fetchall()
            for item in data:
                DATA_PRODUCT[item[0]] = item[1]
            chat_id = message.chat.id
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            # btn3 = types.KeyboardButton("Назад")
            btn4 = types.KeyboardButton("На Главную")
            row = [types.KeyboardButton(x) for x in DATA_PRODUCT.keys()]
            # row.append(btn3)
            row.append(btn4)
            markup.add(*row)
            products = []
            for k, v in DATA_PRODUCT.items():
                products.append(f'{k}. {v}')
            x = '\n'.join(products)
            m = bot.send_message(
                chat_id, text=f"Выберите продукт\n\n{x}", reply_markup=markup)
            bot.register_next_step_handler(m, product_detail)
        product(message)
        #
        # def product_detail(message):
        #     DATA_PRODUCT = {}
        #     cursor = connection.cursor()
        #     cursor.execute(
        #         f'SELECT * FROM product_product where product_product.id = {int(message.text)}'
        #     )
        #     data = cursor.fetchall()
        #
        #     cursor.execute(
        #         f'SELECT * FROM product_productimage where product_productimage.id = {int(message.text)}'
        #     )
        #     data_product_image = cursor.fetchall()
        #
        #     for item in data_product_image:
        #         product_image = "http://127.0.0.1:8000/media/" + item[1]
        #     for item in data:
        #         DATA_PRODUCT[item[0]] = item[1]
        #     chat_id = message.chat.id
        #     product_link = f"http://127.0.0.1:8000/products/{int(message.text)}/"
        #     if int(message.text) in [int(x) for x in DATA_PRODUCT.keys()]:
        #         markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        #         row = [types.KeyboardButton(x) for x in DATA_PRODUCT.keys()]
        #         markup.add(*row)
        #         products = []
        #         for item in data:
        #             try:
        #                 products.append(f' id: {item[0]}\n title: {item[1]}\n description: {item[2]}\n price :'
        #                                 f' {item[3]}\n data created: {item[4]}\n image: {product_image}')
        #             except:
        #                 products.append(f' id: {item[0]}\n title: {item[1]}\n description: {item[2]}\n price :'
        #                                 f' {item[3]}\n data created: {item[4]}\n image: ""')
        #         x = '\n'.join(products)
        #         log_title = [item[1] for item in data]
        #         log_title = '\n'.join(log_title)
        #         m = bot.send_message(
        #             chat_id, text=f'<b>{log_title}</b><pre>{x}</pre>  <b>\n\nLink:{product_link}</b>',
        #             parse_mode='HTML')
        #         bot.register_next_step_handler(m, product_detail)
        #     else:
        #         m = bot.send_message(
        #             chat_id, text=f"Такой продукт отсутствует, пожалуйста выберите другой продукт")
        #         bot.register_next_step_handler(m, product_detail)


bot.infinity_polling()

if __name__ == "__main__":
    print("File one executed when ran directly")

