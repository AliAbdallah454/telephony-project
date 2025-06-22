import cv2
import face_recognition
import pickle
from dotenv import load_dotenv
import os

from my_bot import MyBot

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = MyBot(TELEGRAM_BOT_TOKEN, CHAT_ID)
bot.send_message(["ali"])