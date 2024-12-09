import asyncio
import os
import random
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
from googletrans import Translator

from config import TOKEN

# Константы
API_KEY = "3f198c33cdf3eb519ccddff8be5fedff"
CITY = "Moscow"  # Город для прогноза
bot = Bot(token=TOKEN, timeout=120)
dp = Dispatcher()

translator = Translator()

# Функция для получения прогноза погоды
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"].capitalize()
        return f"Погода в {data['name']}:\nТемпература: {temperature}°C\nСостояние: {description}"
    else:
        return "Не удалось получить данные о погоде. Проверьте город или API-ключ."

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Привет! {message.from_user.first_name}, я бот! Напиши /help, чтобы узнать, что я умею.")

# Команда /help
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Команды:\n"
        "/start - Приветственное сообщение\n"
        "/help - Список доступных команд\n"
        "/weather - Узнать погоду в городе Moscow\n"
        "/video - Отправить видео\n"
        "/doc - Отправить документ\n"
        "/audio - Отправить аудио\n"
        "/training - Получить тренировку"
    )

# Команда /weather
@dp.message(Command("weather"))
async def weather(message: Message):
    weather_report = get_weather()
    await bot.send_chat_action(message.chat.id, "typing")
    await message.answer(weather_report)

# Команда /video
@dp.message(Command("video"))
async def send_video(message: Message):
    try:

        video = FSInputFile("test_video.mp4")
        print(f"Отправка видео началась: {video}")


        async def keep_typing():
            while True:
                await bot.send_chat_action(message.chat.id, "upload_video")
                await asyncio.sleep(3)  # Обновляем индикатор каждые 3 секунды


        typing_task = asyncio.create_task(keep_typing())

        # Пытаемся отправить видео
        await bot.send_video(message.chat.id, video)


        typing_task.cancel()
    except Exception as e:

        typing_task.cancel()
        print(f"Ошибка при отправке видео: {e}")
        await message.answer(f"Ошибка при отправке видео: {str(e)}")

# Команда /doc
@dp.message(Command("doc"))
async def send_doc(message: Message):
    await bot.send_chat_action(message.chat.id, "upload_document")
    doc = FSInputFile("Template.pdf")
    await bot.send_document(message.chat.id, doc)

# Команда /audio
@dp.message(Command("audio"))
async def send_voice(message: Message):
    try:

        voice = FSInputFile("test_voice.ogg")
        print(f"Отправка голоса началась: {voice}")


        async def keep_typing():
            while True:
                await bot.send_chat_action(message.chat.id, "record_audio")
                await asyncio.sleep(3)


        typing_task = asyncio.create_task(keep_typing())


        await bot.send_voice(message.chat.id, voice)


        typing_task.cancel()
    except Exception as e:

        typing_task.cancel()
        print(f"Ошибка при отправке голоса: {e}")
        await message.answer(f"Ошибка при отправке голоса: {str(e)}")

# Команда /training
@dp.message(Command("training"))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений\n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений\n3. Планка с поднятой ногой: 3 подхода по 20 секунд",
        "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша тренировка на сегодня:\n{rand_tr}")

    # Генерация голосового сообщения
    tts = gTTS(text=rand_tr, lang="ru")
    tts.save("training.ogg")
    audio = FSInputFile("training.ogg")
    await bot.send_voice(message.chat.id, audio)
    os.remove("training.ogg")

# Обработка текстовых сообщений для перевода
@dp.message()
async def translate_message(message: Message):
    translated_text = translator.translate(message.text, src="ru", dest="en").text
    await message.answer(f"Перевод на английский: {translated_text}")

# Установка команд в меню
async def set_commands():
    commands = [
        {"command": "start", "description": "Приветственное сообщение"},
        {"command": "help", "description": "Список доступных команд"},
        {"command": "weather", "description": "Узнать погоду в городе Moscow"},
        {"command": "video", "description": "Отправить видео"},
        {"command": "doc", "description": "Отправить документ"},
        {"command": "audio", "description": "Отправить аудио"},
        {"command": "training", "description": "Получить тренировку"}
    ]
    await bot.set_my_commands(commands)

# Главная функция
async def main():
    await set_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())