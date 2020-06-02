from picamera import PiCamera
from time import sleep
import os

def log(msg):
    # Customized print function
    print("> ", end="")
    print(msg)

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
    run_snap_loop(camera)

if __name__ == "__main__":
    main()

