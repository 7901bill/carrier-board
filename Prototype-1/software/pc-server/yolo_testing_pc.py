#Using it: python yolo_testing_pc.py --port 5555 --conf 0.5 --show 0 --classes animal

import argparse
import time
import cv2
import numpy as np
import imagezmq
from ultralytics import YOLO
import zmq  # for catching ZMQError

# COCO class names used by YOLOv8 models
COCO_CLASSES = [
    "person","bicycle","car","motorcycle","airplane","bus","train","truck","boat","traffic light",
    "fire hydrant","stop sign","parking meter","bench","bird","cat","dog","horse","sheep","cow",
    "elephant","bear","zebra","giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee",
    "skis","snowboard","sports ball","kite","baseball bat","baseball glove","skateboard","surfboard",
    "tennis racket","bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple",
    "sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair","couch",
    "potted plant","bed","dining table","toilet","tv","laptop","mouse","remote","keyboard","cell phone",
    "microwave","oven","toaster","sink","refrigerator","book","clock","vase","scissors","teddy bear",
    "hair drier","toothbrush"
]

# Default "animal" subset of COCO class indices
ANIMAL_NAMES = {"bird","cat","dog","horse","sheep","cow","elephant","bear","zebra","giraffe"}
ANIMAL_IDS = {COCO_CLASSES.index(n) for n in ANIMAL_NAMES}

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=5555, help="TCP port to bind (e.g., 5555)")
    p.add_argument("--conf", type=float, default=0.5, help="confidence threshold")
    p.add_argument("--model", type=str, default="yolov8n.pt", help="Ultralytics model file or name")
    p.add_argument("--classes", type=str, default="animal",
                   help='Which classes to alert on. Options: "animal" (default), "all", '
                        'or comma-separated class names e.g. "person,dog".')
    p.add_argument("--show", type=int, default=0, help="1 to visualize frames w/ boxes, else 0")
    p.add_argument("--profile", action="store_true", help="print FPS / timing stats")
    return p.parse_args()

def build_class_filter(arg: str):
    arg = arg.strip().lower()
    if arg == "all":
        return set(range(len(COCO_CLASSES)))
    if arg == "animal":
        return set(ANIMAL_IDS)
    names = [s.strip() for s in arg.split(",") if s.strip()]
    out = set()
    for n in names:
        if n in COCO_CLASSES:
            out.add(COCO_CLASSES.index(n))
    if not out:
        out = set(ANIMAL_IDS)
    return out

def main():
    args = parse_args()
    classes_to_alert = build_class_filter(args.classes)

    image_hub = imagezmq.ImageHub(open_port=f"tcp://*:{args.port}", REQ_REP=True)
    model = YOLO(args.model)

    last = time.time()
    frame_count = 0

    print(f"[Server] Listening on tcp://*:{args.port}")
    print(f"[Server] Model: {args.model}. Alerting on classes: {[COCO_CLASSES[i] for i in sorted(classes_to_alert)]}")

    try:
        while True:
            try:
                sender_name, jpg_buffer = image_hub.recv_jpg()
            except zmq.error.ZMQError as e:
                print(f"[Server] Waiting for client... ({e})")
                time.sleep(1)
                continue

            frame = cv2.imdecode(np.frombuffer(jpg_buffer, dtype=np.uint8), cv2.IMREAD_COLOR)
            results = model.predict(frame, verbose=False, conf=args.conf)
            det = results[0]

            animal_found = False
            if det.boxes is not None and len(det.boxes) > 0:
                for b in det.boxes:
                    cls_id = int(b.cls[0])
                    if cls_id in classes_to_alert:
                        animal_found = True
                        break

            # Reply & logging
            if animal_found:
                print(f"[Server] Frame {frame_count}: DETECTED animal!")
                image_hub.send_reply(b"DETECTED")
            else:
                if frame_count % 30 == 0:  # log OK only every ~30 frames
                    print(f"[Server] Frame {frame_count}: OK (no animal)")
                image_hub.send_reply(b"OK")

            if args.show:
                annotated = det.plot()
                cv2.imshow("Server View (YOLO)", annotated)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            frame_count += 1

            # Optional FPS profiling
            if args.profile and frame_count % 30 == 0:
                now = time.time()
                fps = 30.0 / (now - last)
                last = now
                print(f"[Server] ~{fps:.2f} FPS over last 30 frames")

    finally:
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass

if __name__ == "__main__":
    main()

