from picamera import PiCamera
from time import sleep
import os
import telegram
import numpy as np
import config
import matplotlib.pyplot as plt

# Token stored as a secret and fetched from another file
bot = telegram.Bot(token=config.telegram_bot_token)


def log(msg: str):
    """ Customized print function.
    """
    print("> ", end="")
    print(msg)


def bot_message(msg: str, chat_id: str = config.telegram_chat_id):
    """ Sends custom message through a telegram bot.
    Args:
        - msg: Custom message.
        - chat_id: Target chat ID in format: XXXXXXX.
    """
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
    """ Telegram bot cleanup actions.
    """
    bot_message("Motion detector shutting down!")


def setup_camera() -> PiCamera:
    """ Camera initializer.
    Returns:
        - Camera interface for capturing images.
    """
    cam = PiCamera()
    cam.rotation = 0
    cam.resolution = (1280, 720)
    cam.framerate = 30
    cam.image_effect = 'none'
    cam.exposure_mode = 'auto'
    cam.awb_mode = 'auto'

    log("Setup complete!")
    return cam


def find_img_names(path: str) -> [str]:
    """ Returns found names of the found files with specific filetype.
    Args:
        - path: Target path to search files in.
    Returns:
        - List of file names in format: relative_path/filename.filetype.
    """
    filetype = "jpg"
    return [i for i in os.listdir(path) \
            if ''.join(reversed(i[-1:-4:-1])) == filetype]


def get_img_num(name: str) -> int:
    """ Extracts the image number from its name.
    E.g. image71.jpg -> 71
    Args:
        - name: image name in format imageXXXX.jpg.
    Returns:
        - The extracted number.
    """
    prefix = "image"
    suffix = ".jpg"
    return int(name[len("prefix") : (len(name) - len(suffix))])


def img_to_grayscale(img: np.ndarray) -> np.ndarray:
    """ Converts an RGB image to a grayscale image using
    Luma coding grayscale conversion for RGB images.
    Args:
        - img: RGB image to be converted.
    Return:
        - Conversion result as grayscale image.
    """
    luma_conversion_component = [0.2989, 0.5870, 0.1140]
    gray_converter = lambda rgb: np.dot(rgb[..., :3], luma_conversion_component)

    return gray_converter(img.astype(float))


def get_delta_img(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    delta_img = abs(img_to_grayscale(img1) - img_to_grayscale(img2))
    return (delta_img * 255).astype(uint8)


def count_img_diff(img1: np.ndarray, img2: np.ndarray) -> float:
    """ Given two images, returns a difference percentage.
    Args:
        - img1: An RGB image for comparison.
        - img2: An RGB image for comparison.
    Returns:
        - Difference percentage based on the number of different pixels
          in the image.
    """
    # Allowed pixel level difference
    epsilon = 5.0
    
    delta = img_to_grayscale(img1) - img_to_grayscale(img2)
    pixel_diff = (delta >= epsilon).astype(int)
    diff_percentage = np.count_nonzero(pixel_diff) / np.size(delta)
    return diff_percentage


def capture_img(camera: PiCamera, filename: str):
    """ Takes an image and saves it.
    Args:
        - camera: Camera interface used to take the image.
        - filename: Name of the file to be saved. Overwrites existing files.
    """
    camera.capture(filename)


def run_snap_loop(camera: PiCamera, s_interval: int = 1,
                  n_tempfiles: int = 2, save_location: str = os.getcwd()):
    """ Never ending control loop of the program. Takes images, compares them
    and notifies Telegram.
    Args:
        - camera: Camera interface.
        - s_interval: Wait interval between loops given as seconds.
        - n_tempfiles: Max number of saved images.
        - save_location: Path to the image save folder.
    """
    # Iterator to change file names. Resets back to 0 after
    # reaching n_tempfiles.
    tempfile_num_iter = 0
    
    temp_folder = os.path.join(save_location, "temp")

    diff_from_prev_img = 0.0
    
    # Threshold levels for logging and telegram notification.
    diff_threshold_log = 0.1
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

        if diff_from_prev_img > diff_threshold_log:
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
