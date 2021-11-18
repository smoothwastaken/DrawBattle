import socket
import argparse
import os
import time

parser = argparse.ArgumentParser(description="Start a DrawBattle server with arguments.")
parser.add_argument('-n', '--name', dest="name", metavar="<FILE_NAME>", type=str, help="Specify a file name.")
parser.add_argument('-p', '--port', dest="port", metavar="<PORT>", type=int, help="Specify a port number for send.")

args = parser.parse_args()

print(args)

username = args.name
port = args.port
addr = (socket.gethostbyname(socket.gethostname()), int(port))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP

server.bind(addr)

server.listen()

client_socket, client_address = server.accept()

file_path = f'./notation-website/results/{username}.png'

file = open(file_path, "wb+")
image_chunk = client_socket.recv(2048)

while image_chunk:
    file.write(image_chunk)
    image_chunk = client_socket.recv(2048)

file.close()
client_socket.close()