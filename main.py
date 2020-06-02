from picamera import PiCamera
from time import sleep
import os
import telegram
import numpy as np
import config

# Token stored as a secret and fetched from another file
bot = telegram.Bot(token=config.telegram_bot_token)

def log(msg):
    # Customized print function
    print("> ", end="")
    print(msg)

def bot_message(msg, chat_id=config.telegram_chat_id):
    # Sends a message through the Telegram bot to a specific chat
    bot.sendMessage(chat_id=chat_id, text=msg)

def bot_cleanup():
    # Telegram bot cleanup actions
    bot_message("Motion detector shutting down!")

def setup_camera():
    # Camera initializer
    cam = PiCamera()
    cam.rotation = 0
    cam.resolution = (1280, 720)
    cam.framerate = 30
    cam.image_effect = 'none'
    cam.exposure_mode = 'auto'
    cam.awb_mode = 'auto'

    log("Setup complete!")
    return cam

def count_img_diff(img1, img2):
    # Given two 3-channel images with value range of (0, 255),
    # returns difference percentage based on the number of different pixels.
    # Epsilon controls the allowed pixel level difference.
    epsilon = 10.0
    
    diff = img1 - img2
    pixel_diff = (diff >= epsilon).astype(int)
    diff_percentage = np.count_nonzero(pixel_diff) / np.size(diff)
    return diff_percentage


def capture_img(camera, filename):
    camera.capture(filename)

def run_snap_loop(camera, s_interval=10, n_tempfiles=2,
                  save_location=os.getcwd()):
    tempfile_num_iter = 0

    while True:
        sleep(s_interval)

        # Take a snapshot
        filename = os.path.join(save_location, "temp",
                                "image%s.jpg" %str(tempfile_num_iter))
        capture_img(camera, filename)

        # When iterator reaches n it resets to zero
        tempfile_num_iter = (tempfile_num_iter + 1) % n_tempfiles


def main():
    camera = setup_camera()
    bot_message("Motion detector running!")

    try:
        run_snap_loop(camera)
    finally:
        bot_cleanup()

if __name__ == "__main__":
    main()

