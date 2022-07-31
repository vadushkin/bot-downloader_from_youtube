# System
import re
import os
import datetime
from config import TOKEN

# Add app
import telebot
from pytube import YouTube
from pytube import Playlist

# Token in config.py
token = TOKEN

bot = telebot.TeleBot(token)


def writes_logs(_ex):
    """Записывает логи в файл 'logs.log', в котором будет время и ошибка"""
    with open('logs.log', 'a') as file_log:
        file_log.write('\n' + str(datetime.datetime.now()) + ': ' + str(_ex))


def create_audio(url):
    """Скачивает и открывает файл на бинарное чтение"""
    try:
        yt = YouTube(url).streams.filter(only_audio=True).first()
        path = yt.download("music")
        audio = open(path, 'rb')
        return audio
    except Exception as _ex:
        writes_logs(_ex)


def delete_all_music_in_directory():
    """Удаляет все скаченные аудио из папки 'music'"""
    if not os.path.exists('music'):
        os.mkdir('music')
    for file in os.listdir('music'):
        try:
            if re.search('mp4', file):
                mp4_path = os.path.join('music', file)
                os.remove(mp4_path)
        except Exception as _ex:
            writes_logs(_ex)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Стартовое приветствие"""
    bot.send_message(message.chat.id, "Привет ✌\nПришли мне ссылку на плейлист или видео с YouTube!")


@bot.message_handler(content_types=['text'])
def get_files(message):
    """Ждёт от пользователя ссылку на ютуб плейлист или видео и начинает его скачивать, и отравляет пользователю"""

    if message.text[:38] == 'https://www.youtube.com/playlist?list=':
        # Для плейлиста
        playlist = Playlist(message.text)

        for url in playlist:
            try:
                audio = create_audio(url)
                bot.send_audio(message.chat.id, audio)
            except Exception as _ex:
                writes_logs(_ex)
        else:
            bot.send_message(message.chat.id, "Плейлист закрыт")

    elif message.text[:32] == 'https://www.youtube.com/watch?v=' or message.text[:17] == 'https://youtu.be/':
        # Для видео
        try:
            url = message.text
            audio = create_audio(url)
            bot.send_audio(message.chat.id, audio)
        except Exception as _ex:
            writes_logs(_ex)


delete_all_music_in_directory()
bot.infinity_polling()
