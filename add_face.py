# register_face.py
import cv2
import face_recognition
import pickle
import os

ENCODING_FILE = "encodings.pkl"
FACES_DIR = "faces"

os.makedirs(FACES_DIR, exist_ok=True)

if os.path.exists(ENCODING_FILE):
    with open(ENCODING_FILE, "rb") as f:
        data = pickle.load(f)
else:
    data = {"encodings": [], "names": []}

name = input("Enter your name: ")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera.")
    exit()

print("Press SPACE to capture your face.")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 32:  # SPACE key
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        if encodings:
            top, right, bottom, left = locations[0]
            face_image = frame[top:bottom, left:right]
            cv2.imwrite(f"{FACES_DIR}/{name}.jpg", face_image)
            data["encodings"].append(encodings[0])
            data["names"].append(name)

            with open(ENCODING_FILE, "wb") as f:
                pickle.dump(data, f)
            print(f"✅ Face of {name} saved.")
        else:
            print("No face detected.")
        break

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()