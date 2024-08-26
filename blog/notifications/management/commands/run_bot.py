import os
import telebot
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from notifications.models import Subscriber
from bot.bot import start_bot
class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Bot is running...'))
        start_bot()