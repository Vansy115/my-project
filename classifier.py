from intents.jokes_gen import get_joke
from intents.select_film import select_film
from intents.select_series import select_series
from intents.last_news import last_news
from intents.talking import get_next_sequence
from intents.add_reminder import add_reminder
from intents.weather import weather_handler
from generate.slot_detection_tune import message_to_tag


async def classify(text, user):
    # todo добавить ифы
    tags = await message_to_tag(text)
    print(tags)
    if 'anek' in tags.keys():
        return ['анекдот', await get_joke()]
    elif 'film' in tags.keys():
        return ['фильм', await select_film()]
    elif 'serial' in tags.keys():
        return ['сериал', await select_series()]
    elif 'news' in tags.keys():
        return ['новость', await last_news()]
    elif 'currency' in tags.keys() or 'currency_name' in tags.keys():
        pass
    elif 'reminder' in tags.keys():
        return ['напоминание', await add_reminder(text, tags, user)]
    elif 'weather_descriptor' in tags.keys():
        return ['погода', await weather_handler(text, user)]
    else:
        return ['болталка', await get_next_sequence(text, user, 0)]
