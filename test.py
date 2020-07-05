import cv2
import socket
import struct
import time
import pickle
#import zlib
import errno


IP = '192.168.0.28'
PORT = 8485
HEADER_SIZE = 10

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((IP, PORT))
connection = server_socket.makefile('wb')

cam = cv2.VideoCapture(0)

size_header = server_socket.recv(HEADER_SIZE).decode('utf-8')
size = server_socket.recv(int(size_header))
size = pickle.loads(size)

(width, height) = size


cam.set(3, width)
cam.set(4, height)


img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    # data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)

    try:
        server_socket.sendall(struct.pack(">L", size) + data)
    except Exception as e:
        if e.errno in [errno.EPIPE, errno.ECONNRESET]:
            print('Disconnected from server')
            break
    img_counter += 1

cam.release()
server_socket.close()
