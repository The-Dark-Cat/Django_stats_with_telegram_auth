import asyncio
import os

from aiogram import Bot, Dispatcher, executor, types
from asgiref.sync import sync_to_async
from django.db import transaction
from django.urls import reverse

from UserAuth.models import User, TempToken, UserWhitelist

bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher(bot)


async def set_commands():
    await bot.set_my_commands([
        types.BotCommand(command='start', description='Start'),
        types.BotCommand(command='login', description='Login user'),
    ])

asyncio.get_event_loop().run_until_complete(asyncio.gather(set_commands()))

# set keyboard with register button
def register_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button_register = types.InlineKeyboardButton(text='Register', callback_data='register')
    keyboard.add(button_register)
    return keyboard


@sync_to_async(thread_sensitive=True)
def login_user_from_model(user):
    token = user.get_unique_token()
    TempToken.objects.create(user=user, token=token)
    return os.environ.get('SITE_URL')[:-1] + reverse('custom_user_login', kwargs={'token': token}, current_app='UserAuth')


@sync_to_async(thread_sensitive=True)
def register_user(telegram_id, first_name, last_name, username):
    with transaction.atomic():
        user, created = User.objects.update_or_create(telegram_id=telegram_id,
                                                      defaults={'first_name': first_name,
                                                                'last_name': last_name,
                                                                'username': username})
        if created:
            whitelist = UserWhitelist.objects.get(telegram_id=telegram_id)
            user.keitaro_username = whitelist.keitaro_username
            user.save()

        return user




@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Hi! I'm a bot that helps you to login to site",
                           reply_markup=register_keyboard())


async def login_user(message: types.Message):
    telegram_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    try:
        user = await register_user(telegram_id, first_name, last_name, username)
        url = await login_user_from_model(user)
        keyboard = types.InlineKeyboardMarkup()
        button_login = types.InlineKeyboardButton(text='Login', url=url)
        keyboard.add(button_login)
        await message.answer("You are registered", reply_markup=keyboard)
    except UserWhitelist.DoesNotExist:
        await message.answer("Register denied")
    except TypeError:
        await message.answer("Something went wrong")


@dp.message_handler(commands=['login'])
async def login(message: types.Message):
    await login_user(message)


@dp.callback_query_handler(lambda call: call.data == 'register')
async def register(call: types.CallbackQuery):
    await login_user(call.message)


# run bot

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
