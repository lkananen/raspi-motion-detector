import picamera.PiCamera
from time import sleep
import os

def log(msg):
    print("> ",end="")
    print(msg)

def setup_camera():
    # Camera initializer
    cam = picamera.PiCamera()
    cam.rotation = 0
    cam.resolution = (1280, 720)
    cam.framerate = 30
    cam.image_effect = 'none'
    cam.exposure_mode = 'auto'
    cam.awb_mode = 'auto'

    log("Setup complete!")
    return cam

def main():
    camera = setup_camera()

if __name__ == "__main__":
    main()

