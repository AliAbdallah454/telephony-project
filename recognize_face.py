import cv2
import face_recognition
import pickle
from dotenv import load_dotenv
import os
from PIL import Image
import numpy as np

from my_bot import MyBot
from responses import generate_visitor_message

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = MyBot(TELEGRAM_BOT_TOKEN, CHAT_ID)

ENCODING_FILE = "encodings.pkl"

seen_faces = set()

with open(ENCODING_FILE, "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

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
            if name not in seen_faces:
                seen_faces.add(name)
                message = generate_visitor_message(name)
                bot.send_message([message])
                
                face_image = frame[top:bottom, left:right]
                face_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(face_rgb)
                bot.send_pil_image(pil_image)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()