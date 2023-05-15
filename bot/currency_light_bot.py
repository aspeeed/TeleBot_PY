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
    def create_keyboard():
        keyboard = types.InlineKeyboardMarkup()
        key_joke = types.InlineKeyboardButton(text='Send a joke', callback_data='s_joke')
        keyboard.add(key_joke)
        key_btc_rate = types.InlineKeyboardButton(text='Bitcoin exchange rate', callback_data='btc_rate')
        keyboard.add(key_btc_rate)
        key_the_quiz = types.InlineKeyboardButton(text='The quiz', callback_data='the_quiz')
        keyboard.add(key_the_quiz)
        return keyboard

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == 'Try to mumble something':
            bot.send_message(message.from_user.id, "I want to play a game")
            img = open('src/hello-jigsaw.mp4', 'rb')
            bot.send_video(message.chat.id, img)
            img.close()
            keyboard = create_keyboard()
            bot.send_message(message.from_user.id, "<b>You try to get out, but you realize that you are securely chained to the wall</b>", parse_mode="HTML")
            time.sleep(3)
            bot.send_message(message.from_user.id, "So fast? NO!")
            bot.send_message(message.from_user.id, "You watched a lot of shows on TV. Now I'll show you reality.", reply_markup=keyboard)
            time.sleep(2)
            img2 = open('src/after-saw.mp4', 'rb')
            bot.send_video(message.chat.id, img2)
            img2.close()
        else:
            bot.send_message(message.from_user.id, "Play with me")

        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            if call.data == 's_joke':
                qw2 = requests.get('https://geek-jokes.sameerkumar.website/api?format=json')
                qw2_prs_json = json.loads(qw2.text)
                jk = qw2_prs_json['joke']
                keyboard = create_keyboard()
                bot.send_message(message.from_user.id, jk,reply_markup=keyboard)
            if call.data == 'btc_rate':
                r = requests.get('https://www.rbc.ru/crypto/currency/btcusd')
                soup = BeautifulSoup(r.text, "html.parser")
                data = soup.findAll('span', class_='currencies__td__inner')[1].getText()
                keyboard = create_keyboard()
                bot.send_message(message.from_user.id,"You had economic news with you. Bitcoin exchange rate is " + data, reply_markup=keyboard)
            if call.data == 'the_quiz':
                qw = requests.get('http://jservice.io/api/random?count=1')
                qw_prs_json = json.loads(qw.text)
                qw_qw = qw_prs_json[0]['question']
                answ_answ = qw_prs_json[0]['answer']
                answ_answ = re.sub(r'<[^>]*>', '', answ_answ)
                keyboard_1 = types.InlineKeyboardMarkup()
                btn4 = types.InlineKeyboardButton(text='Jerry', callback_data='Jerry')
                keyboard_1.add(btn4)
                btn5 = types.InlineKeyboardButton(text='1956', callback_data='1956')
                keyboard_1.add(btn5)
                btn6 = types.InlineKeyboardButton(text='its ' + answ_answ, callback_data='its')
                keyboard_1.add(btn6)
                btn7 = types.InlineKeyboardButton(text='Nobody know\'s', callback_data='Nobody')
                keyboard_1.add(btn7)
                bot.send_message(message.from_user.id, qw_qw, reply_markup=keyboard_1)
                img3 = open('src/your-choice-decision.mp4', 'rb')
                bot.send_video(message.chat.id, img3)
                img3.close()
            if call.data == 'its':
                bot.send_message(message.from_user.id, "You win!", reply_markup=create_keyboard())
            elif call.data in ['Jerry', '1956', 'Nobody']:
                bot.send_message(message.from_user.id, "You lose!", reply_markup=create_keyboard())


    # запустим бота
    bot.infinity_polling()

if __name__ == '__main__':
    run_currency_bot("")