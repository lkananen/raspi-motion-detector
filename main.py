from picamera import PiCamera
from time import sleep
import os
import telegram
import numpy as np
import config
import matplotlib.pyplot as plt

# Token stored as a secret and fetched from another file
bot = telegram.Bot(token=config.telegram_bot_token)

def log(msg):
    # Customized print function
    print("> ", end="")
    print(msg)

def bot_message(msg, chat_id=config.telegram_chat_id):
    # Sends a message through the Telegram bot to a specific chat
    
    # Loop in case the sending fails
    max_retries = 5
    for i in range(5):
        try:
            bot.sendMessage(chat_id=chat_id, text=msg)
            break
        except Exception as e:
            print(e)
            sleep(0.3)

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

def find_img_names(path):
    # Returns found filenames
    filetype = "jpg"
    return [i for i in os.listdir(path) \
            if ''.join(reversed(i[-1:-4:-1])) == filetype]

def get_img_num(name):
    # Extracts the image number from its name.
    # E.g. image71.jpg -> 71
    return int(name[len("image") : (len(name) - len(".jpg"))])

def img_to_grayscale(img):
    # Uses Luma coding grayscale conversion for RGB images.
    luma_conversion_component = [0.2989, 0.5870, 0.1140]
    gray_converter = lambda rgb: np.dot(rgb[..., :3], luma_conversion_component)

    return gray_converter(img)

def count_img_diff(img1, img2):
    # Given two 3-channel images with value range of (0, 255),
    # returns difference percentage based on the number of different pixels.
    # Epsilon controls the allowed pixel level difference.
    epsilon = 5
    
    diff = img_to_grayscale(img1) - img_to_grayscale(img2)
    pixel_diff = (diff >= epsilon).astype(int)
    diff_percentage = np.count_nonzero(pixel_diff) / np.size(diff)
    return diff_percentage


def capture_img(camera, filename):
    camera.capture(filename)

def run_snap_loop(camera, s_interval=1, n_tempfiles=2,
                  save_location=os.getcwd()):
    tempfile_num_iter = 0
    temp_folder = os.path.join(save_location, "temp")

    diff_from_prev_img = 0.0
    diff_threshold = 0.1
    diff_threshold_telegram = 0.2

    while True:
        sleep(s_interval)

        # Take a snapshot
        img_filename = os.path.join(temp_folder, \
                                "image%s.jpg" %str(tempfile_num_iter))
        capture_img(camera, img_filename)

        # Compare to previous image if that exists
        prev_image_filename = os.path.join(temp_folder, \
                    "image%s.jpg" %str((tempfile_num_iter - 1) % n_tempfiles))
        if os.path.exists(prev_image_filename):
            img_now = plt.imread(img_filename)
            img_prev = plt.imread(prev_image_filename)
            diff_from_prev_img = count_img_diff(img_now, img_prev)

        if diff_from_prev_img > diff_threshold:
            print("Motion detected!")
            print("Difference: " + str(round(diff_from_prev_img * 100, 1)) + "%")

        if diff_from_prev_img > diff_threshold_telegram:
            bot_message("Object detected!")

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

