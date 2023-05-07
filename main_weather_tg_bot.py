import requests
import datetime
from config import tg_bot_token, open_wither_token
from aiogram import Bot , types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import time
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token= tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands={'start'})
async def start_command(massage: types.Message):
    user_id = massage.from_user.id
    user_name = massage.from_user.first_name
    user_full_name = massage.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await massage.reply(f'Привет!{user_full_name}! Напиши мне название города и я пришлю сводку погоды!')



@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_wither_token}&units=metric'
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно не пойму что там за погода!'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_ot_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])
        await message.reply(f'***{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}***\n'
              f'Погода в городе: {city}\nТемпература:{cur_weather} C° \n '
              f'{wd}\n'
              f'Влажность воздуха:{humidity}%\nДавление:{pressure} мм.рт.ст\nВетер:{wind}м/с '
              f'Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_ot_the_day}\n'
              f'!!*** Хорошего дня***!!'
              )

    except:
        await message.reply('\U00002620 Проверьте назание города\U00002620')


if __name__ == '__main__':
    executor.start_polling(dp)