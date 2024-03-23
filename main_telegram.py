import os
import telebot
from assistants.open_ai_chatbot import OpenAIChatbot

bot = telebot.TeleBot(os.environ.get('TELEGRAM_API_KEY'))
openaiChatbot = OpenAIChatbot()

@bot.message_handler(commands=['start', 'hello', 'hi'])
def send_welcome(message):
    answer = openaiChatbot.interact('Hi')
    bot.reply_to(message, answer)

@bot.message_handler(func=lambda msg: True)
def chat(message):
    answer = openaiChatbot.interact(message.text)
    bot.reply_to(message, answer)

bot.infinity_polling()