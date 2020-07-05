import socket
import cam
import os
import subprocess

IP = '192.168.0.28'
PORT = 1234
HEADER_SIZE = 10
PACKET_SIZE = 8192


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((IP, PORT))

print('Connected to server')


def send_file(filename, server_socket):

    filename_header = f'{len(str(filename)):<{HEADER_SIZE}}'.encode('utf-8')
    server_socket.send(filename_header + str(filename).encode('utf-8')) 

    file = open(f'vids/{filename}.mp4', 'rb')

    full_data = os.stat(f'vids/{filename}.mp4').st_size

    data_header = f'{full_data:<{HEADER_SIZE}}'.encode('utf-8')
    server_socket.send(data_header)

    data = file.read(PACKET_SIZE)    
    while data:
        server_socket.send(data)
        data = file.read(PACKET_SIZE)
        
    print(f'{filename}.mp4 sent successfully')
    file.close()
    command = f'rm vids/{filename}.mp4'
    subprocess.call([command], shell=True)


while True:
    t = input('enter letter ')
    if t.lower() == 't':
        filename = cam.record(cam.camera, 5)
        send_file(filename, server_socket)
    if t.lower() == 'q':
        print('Disconnnecting from server')
        break



server_socket.close()
