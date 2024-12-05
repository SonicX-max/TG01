import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

API_KEY = "3f198c33cdf3eb519ccddff8be5fedff"  # Ваш API-ключ
CITY = "Moscow"  # Город для прогноза

bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_weather():
    """Функция для получения прогноза погоды."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"].capitalize()
        return f"Погода в {data['name']}:\nТемпература: {temperature}°C\nСостояние: {description}"
    else:
        return "Не удалось получить данные о погоде. Проверьте город или API-ключ."


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот. Напиши /help, чтобы узнать, что я умею.")


@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "Команды:\n"
        "/start - Приветственное сообщение\n"
        "/help - Список доступных команд\n"
        "/weather - Узнать погоду в городе Москва"
    )


@dp.message(Command("weather"))
async def weather(message: Message):
    weather_report = get_weather()
    await message.answer(weather_report)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())