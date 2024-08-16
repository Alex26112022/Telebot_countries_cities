import sqlite3

import telebot
import os
from dotenv import load_dotenv
from loguru import logger

from config import path_db, path_logger

rotation = '1 MB'  # максимальный размер лог-файла.
retention = '365 days'  # максимальное время хранения лог-файла.

logger.add(path_logger, format='{time} {level} {message}', level='DEBUG',
           rotation=rotation, retention=retention, compression='zip')

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')


@logger.catch
def main():
    bot = telebot.TeleBot(API_TOKEN)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Салам пополам!")

    @bot.message_handler(func=lambda message: True)
    def echo_message(message):
        print(f'Запрос: {message.json}')
        search_word = message.text.capitalize()
        with sqlite3.connect(path_db) as conn:
            cur = conn.cursor()
            sql_query = "SELECT * FROM capitalize WHERE country LIKE ? OR city LIKE ?"  # noqa

            cur.execute(sql_query, (search_word, search_word))

            result = cur.fetchone()
            print(f'Ответ: {result}\n')
            if result is None:
                bot.reply_to(message,
                             'Извините, но я не нашел информацию о такой стране или городе.')  # noqa
                return

            result_str = (f'Страна: {result[1]}\nСтолица: {result[2]}\n'
                          f'Площадь: {result[3]} кв.м\nНаселение: {result[4]} чел.\n'  # noqa
                          f'Официальный язык: {result[5]}\nВалюта: {result[6]}\n'  # noqa
                          f'Международный телефонный код: {result[7]}\n'
                          f'{result[8]}')

            cur.close()
            conn.commit()

        bot.send_photo(message.chat.id, photo=result[9],
                       caption="Государственный флаг")
        bot.reply_to(message, result_str)

    bot.infinity_polling()


if __name__ == '__main__':
    main()
