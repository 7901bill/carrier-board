import imagezmq
import cv2
from ultralytics import YOLO

image_hub = imagezmq.ImageHub(open_port="tcp://*:5555")

model = YOLO("yolov8n.pt")

# COCO animal classes (ID → name)
COCO_CLASSES = model.names
ANIMAL_CLASSES = {15, 16, 17, 18, 19, 20, 21, 22, 23}  # dog, horse, sheep, cow, elephant, bear, zebra, giraffe

print("PC server running...")

while True:
    rpi_name, frame = image_hub.recv_image()

    # Ensure 3 channels
    if frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    results = model.predict(frame, verbose=False)
    detections = results[0]

    found = None
    for box in detections.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        if conf > 0.5 and cls_id in ANIMAL_CLASSES:
            found = COCO_CLASSES[cls_id]
            break

    if found:
        msg = f"DETECTED:{found}"
        print(f"🐾 Animal detected: {found}")
        image_hub.send_reply(msg.encode())
    else:
        image_hub.send_reply(b"OK")
