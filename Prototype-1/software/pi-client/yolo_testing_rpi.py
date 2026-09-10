#!/usr/bin/env python3
"""
Raspberry Pi client: captures frames from Picamera2, JPEG-encodes them, and sends to PC via imageZMQ.
Prints server reply (b"DETECTED" or b"OK" or other things)

Usage:
  python3 pi_client_sender.py --server-ip 192.168.1.100 --port 5555 --size 640x480 --quality 85
"""
import argparse
import socket
import time
import cv2
import numpy as np
import imagezmq

try:
    from picamera2 import Picamera2
    PICAMERA_AVAILABLE = True
except Exception:
    PICAMERA_AVAILABLE = False

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--server-ip", type=str, required=True, help="PC server IP address")
    p.add_argument("--port", type=int, default=5555, help="PC server port")
    p.add_argument("--size", type=str, default="640x480", help="frame size WxH, e.g. 640x480 or 800x600")
    p.add_argument("--quality", type=int, default=85, help="JPEG quality (0-100)")
    p.add_argument("--fps", type=int, default=0, help="Optional FPS cap; 0 for uncapped (server throttles)")
    p.add_argument("--testcam", action="store_true", help="Use synthetic frames if Picamera2 not available")
    return p.parse_args()

def init_camera(size_wh):
    if not PICAMERA_AVAILABLE:
        return None
    from picamera2 import Picamera2
    picam2 = Picamera2()
    w, h = size_wh
    config = picam2.create_preview_configuration(main={"format":"XRGB8888", "size": (w, h)})
    picam2.configure(config)
    picam2.start()
    time.sleep(1.0)  # warmup
    return picam2

def get_frame(picam2, size_wh, counter):
    if picam2 is not None:
        return picam2.capture_array()
    # Fallback synthetic frame (e.g., when testing on a laptop without camera)
    w, h = size_wh
    img = np.zeros((h, w, 3), dtype=np.uint8)
    cv2.putText(img, f"TEST FRAME {counter}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2, cv2.LINE_AA)
    return img

def main():
    args = parse_args()
    w, h = map(int, args.size.lower().split("x"))
    size_wh = (w, h)

    sender = imagezmq.ImageSender(connect_to=f"tcp://{args.server_ip}:{args.port}", REQ_REP=True)
    rpi_name = socket.gethostname()
    if not isinstance(rpi_name, str):
        rpi_name = str(rpi_name)

    picam2 = None
    if PICAMERA_AVAILABLE and not args.testcam:
        try:
            picam2 = init_camera(size_wh)
        except Exception as e:
            print(f"[Pi] Picamera2 init failed, falling back to synthetic frames: {e}")
            picam2 = None
    else:
        if not PICAMERA_AVAILABLE:
            print("[Pi] Picamera2 is not available. Using synthetic frames (--testcam).")
        else:
            print("[Pi] Using synthetic frames (--testcam).")

    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), int(args.quality)]
    print(f"[Pi] Streaming to tcp://{args.server_ip}:{args.port} at {w}x{h}, JPEG q={args.quality}")
    if args.fps > 0:
        print(f"[Pi] FPS capped at ~{args.fps}")

    try:
        counter = 0
        next_time = time.time()
        frame_interval = (1.0 / args.fps) if args.fps > 0 else 0.0

        while True:
            frame = get_frame(picam2, size_wh, counter)
            # Encode as JPEG
            ok, jpg = cv2.imencode(".jpg", frame, encode_params)
            if not ok:
                print("[Pi] JPEG encode failed; skipping frame")
                continue
            reply = sender.send_jpg(rpi_name, jpg)

            # Handle server reply
            if reply == b"DETECTED":
                print(f":[PI] Frame {counter}: DeTECTED")
            elif reply == b"OK":
                if counter % 30 == 0:
                # Print occasionally to show liveness
                    print(f"[PI] Frame {counter}: OK")
            else:
                print(f"[PI] Frame {counter}: Unknown reply: {reply}")

            counter += 1

            # Optional FPS cap
            if frame_interval > 0:
                next_time += frame_interval
                sleep_for = next_time - time.time()
                if sleep_for > 0:
                    time.sleep(sleep_for)
                else:
                    next_time = time.time()
    finally:
        try:
            if picam2 is not None:
                picam2.stop()
        except Exception:
            pass

if __name__ == "__main__":
    main()

