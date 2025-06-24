import socket
import cv2
import numpy as np
import face_recognition
from dotenv import load_dotenv
import os
from PIL import Image
import pickle

from my_bot import MyBot
from responses import generate_visitor_message

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Initialize bot
bot = MyBot(TELEGRAM_BOT_TOKEN, CHAT_ID)

# Load known face encodings
ENCODING_FILE = "encodings.pkl"
with open(ENCODING_FILE, "rb") as f:
    data = pickle.load(f)
known_encodings = data["encodings"]
known_names = data["names"]

seen_faces = set()

# Socket settings
HOST = '0.0.0.0'
PORT = 5001
def handle_received_frame(frame: np.ndarray):
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

                try:
                    print("sending name ...")
                    message = generate_visitor_message(name)
                    bot.send_message([message])
                except Exception as e:
                    print(f"⚠️ Failed to send message: {e}")

                try:
                    face_image = frame[top:bottom, left:right]
                    face_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(face_rgb)
                    print("sending image ...")
                    bot.send_pil_image(pil_image)
                except Exception as e:
                    print(f"⚠️ Failed to send image: {e}")

        # Optional: draw on frame (for debugging)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()

        print(f"📡 Server listening on {HOST}:{PORT}...")

        while True:
            conn, addr = server.accept()
            with conn:
                print(f"📥 Connection from {addr}")

                size_data = conn.recv(4)
                if not size_data:
                    continue

                img_size = int.from_bytes(size_data, byteorder='big')
                img_bytes = b''
                while len(img_bytes) < img_size:
                    chunk = conn.recv(min(4096, img_size - len(img_bytes)))
                    if not chunk:
                        break
                    img_bytes += chunk

                np_arr = np.frombuffer(img_bytes, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                if frame is not None:
                    handle_received_frame(frame)
                else:
                    print("❌ Failed to decode received image.")

if __name__ == "__main__":
    start_server()
