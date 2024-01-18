import os
import requests
from telebot import TeleBot
from radiojavanapi import Client
from moviepy.editor import VideoFileClip

bot = TeleBot('BOT_TOKEN')

@bot.message_handler(commands=['start','help'])
def handle_start(message):
  try:
    bot.send_message(message.chat.id, f"سلام به ربات خوش اومدی\nلینکتو بفرست تا برات دانلودش کنم")
  except Exception as e:
    bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(func=lambda message: message.text.startswith("https://play.radiojavan.com/song"))
def handle_song_link(message):
    try:
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
                caption=f"Name: {song.name}\nArtist: {song.artist}\nPower By : @TrwDev"
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
                caption=f"Title: {podcast.title}\nPower By : @TrwDev"
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
                caption=f"Title: {video.title}\nPower By : @TrwDev"
            )

        os.remove(video_file_path)

        bot.delete_message(message.chat.id, download_message.message_id)
        bot.send_message(message.chat.id, "<b>Download Finished</b>", parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

bot.polling()
