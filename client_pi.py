import cv2
import time
import socket

SERVER_IP = '192.168.0.107'  # Replace with your laptop's IP
SERVER_PORT = 5001

def capture_and_send():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not accessible.")
        return

    last_sent = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture image.")
            continue

        # Show live video feed
        cv2.imshow("Live Camera Feed", frame)

        # Send frame every 2 seconds
        if time.time() - last_sent >= 2.0:
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()
            img_size = len(img_bytes)

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((SERVER_IP, SERVER_PORT))
                    s.sendall(img_size.to_bytes(4, byteorder='big'))
                    s.sendall(img_bytes)
                    print("📤 Frame sent.")
            except Exception as e:
                print(f"🔌 Connection error: {e}")

            last_sent = time.time()

        # Quit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_send()

