import os
import telebot
from dotenv import load_dotenv
from .check import check_if_string_correct
from notifications.models import Subscriber
from categories.models import Category
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
    /cats - изменить категории
    '''
    bot.send_message(message.chat.id, f"Вот список команд: {text}")


#subscription handlers
@bot.message_handler(commands=['subscribe',])
def subscribe(message):
    exists = Subscriber.objects.filter(chat_id=message.chat.id).exists()
    if exists:
        bot.reply_to(message, "Вы уже подписаны если хотите изменить категории используйте /cats")
    else:
        bot.send_message(message.chat.id, "Добрый день, для подписки выберите интересующие категории")
        username = message.from_user.username
        chat_id = message.chat.id
        categories = Category.objects.all()
        text = "Доступные категории введите номера интересующих через пробел:\n "
        counter = 1
        for i in categories:
            text += f"{counter}. {i.name}\n"
            counter += 1
        bot.reply_to(message, text)
        bot.register_next_step_handler(message, register_categories)

def register_categories(message):
    msg_text = message.text
    username = message.from_user.username
    chat_id = message.chat.id
    subscriber = Subscriber.objects.create(username=username, chat_id=chat_id)
    if not check_if_string_correct:
        bot.reply_to(message, "Вы ввели в неправильном формате, введите /cats и попробуйте снова")
    else:
        a = msg_text.split()
        a = map(int, a)
        count = Category.objects.count()
        subscriber.categories.clear()
        counter = 1
        cats = Category.objects.all()
        for cat in cats:
            if counter in a:
                subscriber.categories.add(cat)
            counter += 1
        bot.reply_to(message, 'Спасибо за подписку')





@bot.message_handler(commands=['unsubscribe', ])
def unsubscribe(message):
    subscriber = Subscriber.objects.filter(chat_id=message.chat.id)
    if subscriber.exists():
        bot.reply_to(message, "Вы отписались от блога. Спасибо, что были с нами!")
        subscriber.delete()
    else:
        bot.send_message(message.chat.id, "Вы не подписаны")

@bot.message_handler(commands=['cats', ])
def change_cats(message):
    exists = Subscriber.objects.filter(chat_id=message.chat.id).exists()
    if not exists:
        bot.reply_to(message, 'Сначала подпишитесь через /subscribe')
    else:
        bot.send_message(message.chat.id, "Добрый день, для подписки выберите интересующие категории")
        username = message.from_user.username
        chat_id = message.chat.id
        categories = Category.objects.all()
        text = "Доступные категории введите номера интересующих через пробел:\n "
        counter = 1
        for i in categories:
            text += f"{counter}. {i.name}\n"
            counter += 1
        bot.reply_to(message, text)
        bot.register_next_step_handler(message, register_categories_cats)
def register_categories_cats(message):
    msg_text = message.text
    username = message.from_user.username
    chat_id = message.chat.id
    subscriber = Subscriber.objects.get(chat_id=chat_id)
    if not check_if_string_correct:
        bot.reply_to(message, "Вы ввели в неправильном формате, введите /cats и попробуйте снова")
    else:
        a = msg_text.split()
        a = list(map(int, a))
        count = Category.objects.count()
        subscriber.categories.clear()
        counter = 1
        cats = Category.objects.all()
        for cat in cats:
            print(a, counter)
            if counter in a:
                subscriber.categories.add(cat)
            counter += 1
        bot.reply_to(message, 'Категории изменены')


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

def start_bot():
    bot.infinity_polling()

