import picamera
import subprocess
from datetime import datetime

timestamp = datetime.now().strftime('%d%m%y_%H%M%S')
filename = f'/home/pi/files/prod/vids/{timestamp}'

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25


def record(camera, time):

    timestamp = datetime.now().strftime('%d%m%y_%H%M%S')
    filename = f'/home/pi/files/prod/vids/{timestamp}'

    camera.start_recording(f'{filename}.h264')
    camera.wait_recording(time)
    camera.stop_recording()

    command = f'MP4Box -add {filename}.h264 {filename}.mp4'
    subprocess.call([command], shell=True)
    command = f'rm {filename}.h264'
    subprocess.call([command], shell=True)

    return timestamp
