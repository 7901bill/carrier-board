from picamera2 import Picamera2
import imagezmq
import socket
import time

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main = {"format": 'XRGB8888', "size': (640x480)})
picam2.start()
time.sleep(2)

sender = imagezmq.ImageSender(connect_to = "server-ip":5555)
rpi_name = socket.gethostname()

esp32_ip = "esp32-ip"
esp32_port = 5005
sock_et = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("RPI is running")

while True:
  frame = picam2.capture_array()
  reply = sender.send_image(rpi_name, frame)

  if reply.startswith(b"DETECTED"):
    print("Forwarding detection:", reply.decode())
    sock.sendto(reply, (esp32_ip, esp32_port)
