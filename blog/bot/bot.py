import os
import telebot
from dotenv import load_dotenv
from notifications.models import Subscriber

# Load environment variables
load_dotenv()

TELEKEY = os.getenv('TELEKEY')

if not TELEKEY:
    raise ValueError("TELEKEY is not set in environment variables.")

bot = telebot.TeleBot(TELEKEY)

@bot.message_handler(commands=['start',])
def send_welcome(message):
    bot.reply_to(message, """
    Добро пожаловать в бота моего блога, наберите /help для списка команд
    """)

@bot.message_handler(commands=['help',])
def send_help(message):
    text = '''
    /subscribe - подписаться на рассылку
    /unsubscribe - отписаться отписаться от рассылки
    '''
    bot.send_message(message.chat.id, f"Вот список команд: {text}")

@bot.message_handler(commands=['subscribe',])
def subscribe(message):
    exists = Subscriber.objects.filter(chat_id=message.chat.id).exists()
    if exists:
        bot.reply_to(message, "Вы уже подписаны")
    else:
        bot.send_message(message.chat.id, "Спасибо за подписку!")
        username = message.from_user.username
        chat_id = message.chat.id
        Subscriber.objects.create(username=username, chat_id=chat_id)
@bot.message_handler(commands=['unsubscribe', ])
def unsubscribe(message):
    subscriber = Subscriber.objects.filter(chat_id=message.chat.id)
    if subscriber.exists():
        bot.reply_to(message, "Вы отписались от блога. Спасибо, что были с нами!")
        subscriber.delete()
    else:
        bot.send_message(message.chat.id, "Вы не подписаны")
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

def start_bot():
    bot.infinity_polling()

