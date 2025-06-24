import cv2
import time
import socket

SERVER_IP = '192.168.1.100'  # Replace with your laptop's IP
SERVER_PORT = 5001

def capture_and_send():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not accessible.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture image.")
            continue

        # Show captured image on the screen
        cv2.imshow("Captured Image", frame)

        # Encode and send the image
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()
        img_size = len(img_bytes)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((SERVER_IP, SERVER_PORT))
                s.sendall(img_size.to_bytes(4, byteorder='big'))
                s.sendall(img_bytes)
        except Exception as e:
            print(f"🔌 Connection error: {e}")

        # Break if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(2)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_send()
