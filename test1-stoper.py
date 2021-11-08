import socket
import argparse

parser = argparse.ArgumentParser(description="Start a DrawBattle server with arguments.")
parser.add_argument('-H', '--host', metavar="<HOST>", type=str, help="Specify an ip number for the room to join.")
parser.add_argument('-p', '--port', metavar="<PORT>", type=int, help="Specify a port number for the room to join.")

args = parser.parse_args()

PORT = args.port
HEADER = 128
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!leave"
START_RECEIVING_RESULTS = "!sending-result"
STOP_RECEIVING_RESULTS = "!stop-sending-result"
MAX_USERNAME_LENGHT = 16
SERVER = args.host
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

msg = "%stop"
message = msg.encode(FORMAT)
msg_length = len(message)
send_length = str(msg_length).encode(FORMAT)
send_length += b' ' * (HEADER - len(send_length))
client.send(send_length)
client.send(message)