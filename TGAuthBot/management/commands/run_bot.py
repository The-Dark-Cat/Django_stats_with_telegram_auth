from aiogram.utils import executor
from django.core.management import BaseCommand

from TGAuthBot.bot import dp


class Command(BaseCommand):
    help = 'Run bot'

    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=True)

