import logging
import time
import json
import re
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

# добавим логгирование, чтобы получать сообщения в консоль
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


def run_currency_bot(token: str) -> None:
    """Run simple telegram bot."""
    bot = telebot.TeleBot(token, parse_mode=None)

    # добавим Handler, обрабатывающий команду start
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        """ Respond to a /start message. """
        bot.send_message(message.from_user.id, "📺")
        bot.reply_to(message, "Hello! You don't look happy. What's wrong?")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Try to mumble something")
        markup.add(btn1)
        bot.reply_to(message, "Maybe you don't like the chains on your hands? Or is the room too dark?", reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == 'Try to mumble something':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn3 = types.KeyboardButton("❌ Get out ❌")
            markup.add(btn3)
            bot.send_message(message.from_user.id, "I want to play a game", reply_markup=markup)
            img = open('src/hello-jigsaw.mp4', 'rb')
            bot.send_video(message.chat.id, img)
            img.close()
        elif message.text == '❌ Get out ❌':
            bot.send_message(message.from_user.id, "<b>You try to get out, but you realize that you are securely chained to the wall</b>", parse_mode="HTML")
            time.sleep(3)
            bot.send_message(message.from_user.id, "So fast? NO!")
            bot.send_message(message.from_user.id, "You watched a lot of shows on TV. Now I'll show you reality.")
            time.sleep(2)
            bot.send_message(message.from_user.id, "Let's start")
            img2 = open('src/after-saw.mp4', 'rb')
            bot.send_video(message.chat.id, img2)
            img2.close()
            #обращаемся к апи ресурса с гиковскими шутками
            qw1 = requests.get('https://geek-jokes.sameerkumar.website/api?format=json')
            qw1_prs_json = json.loads(qw1.text)
            jk = qw1_prs_json['joke']
            bot.send_message(message.from_user.id, jk)
            time.sleep(2)
            bot.send_message(message.from_user.id, "<i>channel switching sound</i>", parse_mode="HTML")
            time.sleep(2)
            #парсим сайт рбк и смотрим курс BTC
            r = requests.get('https://www.rbc.ru/crypto/currency/btcusd')
            soup = BeautifulSoup(r.text, "html.parser")
            data = soup.findAll('span', class_='currencies__td__inner')[1].getText()
            bot.send_message(message.from_user.id, "You had economic news with you. Bitcoin exchange rate is " + data)
            time.sleep(2)
            bot.send_message(message.from_user.id, "<i>channel switching sound</i>", parse_mode="HTML")
            time.sleep(2)
            img3 = open('src/confess-tricycle.mp4', 'rb')
            bot.send_video(message.chat.id, img3)
            img3.close()
            bot.send_message(message.from_user.id, "And now we come to the most important part - the quiz. If you answer my question correctly, I will let you go. If not, you will pay a high price")
            time.sleep(2)
            #получаем рандомный ввпрос и ответ
            qw = requests.get('http://jservice.io/api/random?count=1')
            qw_prs_json = json.loads(qw.text)
            qw_qw = qw_prs_json[0]['question']
            answ_answ = qw_prs_json[0]['answer']
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn4 = types.KeyboardButton("Jerry")
            btn5 = types.KeyboardButton("1956")
            btn6 = types.KeyboardButton("its " + answ_answ)
            btn7 = types.KeyboardButton("Nobody know's")
            markup.add(btn4,btn5,btn6,btn7)
            bot.send_message(message.from_user.id, qw_qw,reply_markup=markup)
            img3 = open('src/your-choice-decision.mp4', 'rb')
            bot.send_video(message.chat.id, img3)
            img3.close()
        elif message.text.startswith("its "):
            bot.send_message(message.from_user.id, "You win, get out")
            bot.send_message(message.from_user.id,"<b>You were close to losing consciousness. You woke up from the bright sunlight somewhere in a field near the city...</b>",parse_mode="HTML")
        elif message.text == 'Jerry' or '1956' or 'Nobody know\'s':
            bot.send_message(message.from_user.id, "You lose!")
            bot.send_message(message.from_user.id,"<b>You were close to losing consciousness. And no one else saw you...</b>",parse_mode="HTML")



    # запустим бота
    bot.infinity_polling()

if __name__ == '__main__':
    run_currency_bot("")