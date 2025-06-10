import telebot
import random
from telebot import types

API_TOKEN = '8157646989:AAF2sJ_kvnJK9cN8Zk2HK9Dq84Ybv7ArzJ8'
bot = telebot.TeleBot(API_TOKEN)
counter_user = 0
counter_bot = 0

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_rock = telebot.types.InlineKeyboardButton(text="Rock", callback_data='Камень')
    button_paper = telebot.types.InlineKeyboardButton(text="Paper", callback_data='Бумага')
    button_scissors = telebot.types.InlineKeyboardButton(text="Scissors", callback_data='Ножницы')
    keyboard.add(button_rock, button_paper, button_scissors)
    bot.send_message(message.chat.id, "Привет! Давайте сыграем в 'Камень, ножницы, бумага'. Выберите свой ход:", reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "You choice one of three items from below:\n\n" "Rock, Paper, Scissors.\n\n" "After that I'll randomly pick one of these items too. Each item has one that loses to, and other one that beats beats it.\n\n" "Rock beats Scissors ; Scissors beats Paper ; Paper beats Rock.\n\n" "/start")


@bot.callback_query_handler(func=lambda call: call.data in ['Камень', 'Ножницы', 'Бумага'])
def play_game(call):
    global counter_user, counter_bot
    message = call.message
    user_choice = call.data
    bot_choice = random.choice(['Камень', 'Ножницы', 'Бумага'])
    if counter_bot < 3 and counter_user < 3:
        if user_choice == bot_choice:
            result = 'Ничья!'
        elif (user_choice == 'Камень' and bot_choice == 'Ножницы' or
            user_choice == 'Ножницы' and bot_choice == 'Бумага' or
            user_choice == 'Бумага' and bot_choice == 'Камень'):
            result = 'Вы выиграли!'
            counter_user += 1
        else:
            result = 'Вы проиграли!'
            counter_bot += 1
        bot.send_message(message.chat.id, f"Вы выбрали: {user_choice}\nБот выбрал: {bot_choice}\nРезультат: {result}")
        bot.send_message(message.chat.id, f"Ваш счёт:\nUser = {counter_user},       Bot = {counter_bot}")
    else:
        if counter_bot > counter_user:
            bot.send_message(message.chat.id, "Вы проиграли")
        else:
            bot.send_message(message.chat.id, "Вы выйграли")
        counter_bot = 0
        counter_user = 0
        bot.send_message(message.chat.id, "Если вы хотите сыграть ещё раз, напишите /start")
bot.infinity_polling()