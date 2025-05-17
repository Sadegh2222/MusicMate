import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN
from downloader import download_spotify, download_youtube, download_soundcloud
from lyrics_handler import get_lyrics
import os

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! اسم آهنگ رو بفرست تا دانلود کنم یا متنش رو بیارم.")

@bot.message_handler(func=lambda m: True)
def handle_song_query(message):
    song_name = message.text
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("اسپاتیفای", callback_data=f"spotify|{song_name}"),
        InlineKeyboardButton("یوتیوب", callback_data=f"youtube|{song_name}"),
        InlineKeyboardButton("ساندکلاد", callback_data=f"soundcloud|{song_name}"),
        InlineKeyboardButton("متن آهنگ", callback_data=f"lyrics|{song_name}")
    )
    bot.send_message(message.chat.id, "از کجا دانلود کنم یا متن رو بیارم؟", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    action, song_name = call.data.split('|', 1)
    if action == "spotify":
        bot.send_message(call.message.chat.id, "در حال دانلود از اسپاتیفای...")
        file_path = download_spotify(song_name)
        if file_path and os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                bot.send_audio(call.message.chat.id, f)
        else:
            bot.send_message(call.message.chat.id, "دانلود ناموفق بود.")
    elif action == "youtube":
        bot.send_message(call.message.chat.id, "در حال دانلود از یوتیوب...")
        file_path = download_youtube(song_name)
        if file_path and os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                bot.send_audio(call.message.chat.id, f)
        else:
            bot.send_message(call.message.chat.id, "دانلود ناموفق بود.")
    elif action == "soundcloud":
        bot.send_message(call.message.chat.id, "در حال دانلود از ساندکلاد... (در حال توسعه)")
    elif action == "lyrics":
        lyrics = get_lyrics(song_name)
        bot.send_message(call.message.chat.id, lyrics)

bot.polling() 