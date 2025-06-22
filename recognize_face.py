import cv2
import face_recognition
import pickle
from dotenv import load_dotenv
import os
from PIL import Image
import numpy as np
import threading
import time
from queue import Queue
from my_bot import MyBot
from responses import generate_visitor_message

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ENCODING_FILE = "encodings.pkl"
COOLDOWN_SECONDS = 15  # 5 minutes

bot = MyBot(TELEGRAM_BOT_TOKEN, CHAT_ID)

with open(ENCODING_FILE, "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

message_queue = Queue()
last_sent_time = {}

def bot_worker():
    while True:
        name, image = message_queue.get()
        if name not in last_sent_time or time.time() - last_sent_time[name] > COOLDOWN_SECONDS:
            last_sent_time[name] = time.time()
            message = generate_visitor_message(name)
            bot.send_message([message])
            bot.send_pil_image(image)
        message_queue.task_done()

# Start the bot thread
threading.Thread(target=bot_worker, daemon=True).start()

# Open the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera.")
    exit()

print("Recognizing faces. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for (top, right, bottom, left), face_encoding in zip(locations, encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            best_match = matches.index(True)
            name = known_names[best_match]

            # Only queue if cooldown expired
            if name not in last_sent_time or time.time() - last_sent_time[name] > COOLDOWN_SECONDS:
                face_image = frame[top:bottom, left:right]
                face_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(face_rgb)
                message_queue.put((name, pil_image))

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
