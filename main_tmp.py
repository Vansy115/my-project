# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

import logging

from api.geocoder import *
from api.static_maps import get_toponym_map_url
from api.weather import get_weather

from utils.utils import get_loc_from_doc, text2doc, get_date_diff_from_message

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


@dp.message_handler()
async def message_handler(message: types.Message):
    if 'погода' not in message.text.lower():
        return

    doc = text2doc(message.text)
    loc = get_loc_from_doc(doc)
    diff = get_date_diff_from_message(message.text)

    if loc is None:
        await message.answer('Я не нашёл локацию, извините.')
        return

    if diff < 0:
        await message.answer('Я нашёл дату, которая выходит за диапазон возможных.')
        return

    toponym = await get_toponym(loc)
    # await message.answer("```" + json.dumps(res, indent=4, ensure_ascii=False) + "```", parse_mode='markdown')

    if toponym is not None:
        weather = (await get_weather(*get_toponym_coords(toponym), diff))[diff - 1]

        date_str = weather['date'].strftime('%d.%m.%Y')
        await message.answer_photo(
            get_toponym_map_url(toponym),
            f'*{weather["emoji"]} Погода в {get_toponym_name(toponym)} на {date_str}*\n'
            f'*{weather["condition"].capitalize()}*\n'
            f'*Температура*: {weather["temperature"]} °C\n'
            f'*Атмосферное давление*: {weather["pressure"]} мм рт. ст.\n'
            f'*Влажность*: {weather["humidity"]}%.\n'
            f'*Скорость ветра*: {weather["wind_speed"]} м/с, {weather["wind_dir"]}.\n',
            parse_mode='markdown'
        )
    else:
        await message.answer('Я не понял Ваc, извините.')


executor.start_polling(dp, skip_updates=True)
