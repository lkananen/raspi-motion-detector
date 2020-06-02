from picamera import PiCamera
import time
import os

def setup_cam():
    # Camera initializer
    camera = PiCamera()
    camera.rotation = 0
    camera.resolution = (1280, 720)
    camera.framerate = 30
    camera.image_effect = 'none'
    camera.exposure_mode = 'auto'
    camera.awb_mode = 'auto'

    print("Setup complete!")
    return camera

def run_cam(camera, s_time):
    # Runs a preview for s seconds
    camera.start_preview()
    time.sleep(s_time)
    camera.stop_preview()

def snap(camera, location):
    # Takes a single snapshot
    camera.capture(location)

def snaps(camera, loc=os.getcwd(), n_imgs=1, wait_interval=0):
    # Takes n smapshots and by default saves them to current working directory
    for i in range(n_imgs):
        filename = os.path.join(loc, "image%s.jpg" % i)
        time.sleep(wait_interval)

        snap(camera, filename)
        print("Saved: " + str(filename))

def rec(camera, loc=os.getcwd(), s_length=1, with_preview=False):
    # Records for s seconds.
    c = camera
    filename = os.path.join(loc, "video.h264")

    if with_preview:
        c.start_preview()


    c.start_recording(filename)
    time.sleep(s_length)
    c.stop_recording()

    if with_preview:
        c.stop_preview()

def main():
    camera = setup_cam()

    run_camera(5)
    snaps(camera, n_imgs=5)
    rec(camera)

    print("Success!")

if __name__ == '__main__':
    main()

