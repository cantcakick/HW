from picamera2 import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
for i in range(5):
    sleep(5)
    camera.capture('/home/pi/Desktop/Camera/image%s.jpg' % i)
camera.stop_preview()
