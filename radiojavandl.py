import os
import requests
from telebot import types
from telebot import TeleBot
from radiojavanapi import Client
from moviepy.editor import VideoFileClip

bot = TeleBot('BOT_TOKEN') # <----- توکن ربات شما
channel_username = "CHANNEL_ID" # <------ آیدی چنل اسپانسری
bot_username = "BOT_USERNAME" # <------ یوزر نیم ربات

def check_channel_membership(user_id):
    chat_member = bot.get_chat_member(channel_username, user_id)
    return chat_member.status in ["member", "administrator", "creator"]

def verify_commands(message):
    user_id = message.from_user.id
    if not check_channel_membership(user_id):
        channel_username_cleaned = channel_username.lstrip('@')
        keyboard = types.InlineKeyboardMarkup()
        
        url_button = types.InlineKeyboardButton(text="🔗 عضویت در کانال", url=f"https://t.me/{channel_username_cleaned}")
        keyboard.add(url_button)

        url_button2 = types.InlineKeyboardButton(text="عضو شدم ✅", url=f"https://t.me/{bot_username}?start=welcome")
        keyboard.add(url_button2)

        bot.reply_to(message, f"▫️شما در کانال اسپانسر عضو نیستید\nعضو شوید و سپس /start را بفرستید", reply_markup=keyboard)
        return "Nist"

@bot.message_handler(commands=['start','help'])
def handle_start(message):
  try:
    if verify_commands(message) == "Nist":
        pass
    else:
        bot.send_message(message.chat.id, f"سلام به ربات خوش اومدی\nلینکتو بفرست تا برات دانلودش کنم")
  except Exception as e:
    bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(func=lambda message: message.text.startswith("https://play.radiojavan.com/song"))
def handle_song_link(message):
    try:
        if verify_commands(message) == "Nist":
            pass
        else:
            song_url = message.text

            download_message = bot.send_message(message.chat.id, "Download started...")

            client = Client()
            song = client.get_song_by_url(song_url)

            photo_file = requests.get(song.photo)
            photo_file_path = f"{song.name}_{song.artist}_photo.jpg"

            with open(photo_file_path, "wb") as file:
                file.write(photo_file.content)

            with open(photo_file_path, "rb") as file:
                bot.send_photo(
                    message.chat.id,
                    file
                )

            mp3_file = requests.get(song.hq_link)
            mp3_file_path = f"{song.name}_{song.artist}.mp3"

            with open(mp3_file_path, "wb") as file:
                file.write(mp3_file.content)

            with open(mp3_file_path, "rb") as file:
                audio_message = bot.send_audio(
                    message.chat.id,
                    file,
                    caption=f"Name: {song.name}\nArtist: {song.artist}\nPower By : {channel_username}"
                )

            os.remove(photo_file_path)
            os.remove(mp3_file_path)

            bot.delete_message(message.chat.id, download_message.message_id)
            bot.send_message(message.chat.id, "<b>Download Finished</b>", parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(func=lambda message: message.text.startswith("https://play.radiojavan.com/podcast"))
def handle_podcast_link(message):
    try:
        if verify_commands(message) == "Nist":
            pass
        else:
            podcast_url = message.text

            download_message = bot.send_message(message.chat.id, "Download started...")

            client = Client()
            podcast = client.get_podcast_by_url(podcast_url)

            photo_file = requests.get(podcast.photo)
            photo_file_path = f"{podcast.title}_photo.jpg"

            with open(photo_file_path, "wb") as file:
                file.write(photo_file.content)

            with open(photo_file_path, "rb") as file:
                bot.send_photo(
                    message.chat.id,
                    file
                )

            podcast_file = requests.get(podcast.hq_link)
            podcast_file_path = f"{podcast.title}_podcast.mp3"

            with open(podcast_file_path, "wb") as file:
                file.write(podcast_file.content)

            with open(podcast_file_path, "rb") as file:
                audio_message = bot.send_audio(
                    message.chat.id,
                    file,
                    caption=f"Title: {podcast.title}\nPower By : {channel_username}"
                )

            os.remove(photo_file_path)
            os.remove(podcast_file_path)

            bot.delete_message(message.chat.id, download_message.message_id)
            bot.send_message(message.chat.id, "<b>Download Finished</b>", parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(func=lambda message: message.text.startswith("https://play.radiojavan.com/video"))
def handle_video_link(message):
    try:
        if verify_commands(message) == "Nist":
            pass
        else:
            video_url = message.text

            download_message = bot.send_message(message.chat.id, "Download started...")

            client = Client()
            video = client.get_video_by_url(video_url)

            video_file = requests.get(video.lq_link)
            video_file_path = f"{video.title}_video.mp4"

            with open(video_file_path, "wb") as file:
                file.write(video_file.content)

            target_size_bytes = 45 * 1024 * 1024

            while os.path.getsize(video_file_path) > target_size_bytes:
                compressed_file_path = f"{video.title}_compressed_video.mp4"

                video_clip = VideoFileClip(video_file_path)
                video_clip_resized = video_clip.resize(width=640, height=480)
                video_clip_resized.write_videofile(compressed_file_path, codec="libx264", audio_codec="aac")

                os.remove(video_file_path)
                video_file_path = compressed_file_path

            with open(video_file_path, "rb") as file:
                video_message = bot.send_video(
                    message.chat.id,
                    file,
                    caption=f"Title: {video.title}\nPower By : {channel_username}"
                )

            os.remove(video_file_path)

            bot.delete_message(message.chat.id, download_message.message_id)
            bot.send_message(message.chat.id, "<b>Download Finished</b>", parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

bot.polling()
