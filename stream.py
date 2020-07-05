import socket
import time
import picamera
import subprocess

IP = '192.168.0.28'
PORT = 1234
HEADER_SIZE = 10
PACKET_SIZE = 8192

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.connect((IP, PORT))

client_socket = socket.socket()
client_socket.connect((IP, PORT))

connection = client_socket.makefile('wb')

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 25
        camera.start_preview()
        time.sleep(2)
        camera.start_recording('temp.h264', format='h264')
        camera.wait_recording(60)
        camera.stop_recording()

        command = 'MP4Box -add temp.h264 temp.mp4'
        subprocess.call([command], shell=True)

        temp = open('temp.mp4', 'rb')

        connection.write(temp.read())

        temp.close()

        command = 'rm temp.mp4 temp.h264'
        subprocess.call([command], shell=True)
        
        

finally:
    connection.close()
    client_socket.close()
