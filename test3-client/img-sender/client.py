import socket
import argparse

parser = argparse.ArgumentParser(description="Start a DrawBattle server with arguments.")
parser.add_argument('-p', '--port', metavar="<PORT>", type=int, help="Specify a port number for send.")

args = parser.parse_args()

port = args.port
addr = (socket.gethostbyname(socket.gethostname()), int(port))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect(addr)  # 127.0.0.1

file = open(f'./result.png', "rb")
image_data = file.read(2048)

while image_data:
    client.send(image_data)
    image_data = file.read(2048)

file.close()
client.close()