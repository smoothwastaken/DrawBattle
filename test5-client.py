import socket
import threading
import turtle as tt
# import keyboard
import os
import argparse
import random
import time
import subprocess
from PIL import Image

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
IMAGE_SENDER_FILE = "img-sender/client.py"
OS = ""
MAX_USERNAME_LENGHT = 16
SERVER = args.host
ADDR = (SERVER, PORT)

END_PLAYING = 0

turtle = tt.Turtle()



def save_as_png(canvas,fileName):
    # save postscipt image
    print(f"""⏳ - Saving the Tkinter's canvas as .eps file...""")
    canvas.postscript(file = fileName + '.eps')
    print(f"""✅ - Tkinter's canvas saved""")
    # use PIL to convert to PNG
    print(f"""⏳ - Opening eps canvas...""")
    img = Image.open(fileName + '.eps')
    print(f"""✅ - Tkinter's eps canvas saved""")
    print(f"""⏳ - Converting eps Tkinter's canvas in png...""")
    img.save(fileName + '.png', 'png')
    print(f"""✅ - Tkinter's eps canvas converted to png""")


class Player():
    def __init__(self):
        print(f"""⏳ - Creating player's instance...""")
        print(f"""✅ - Player's instance created.""")

    def turn_right(self, p):
        p.right(5)
        return

    def turn_left(self, p):
        p.left(5)
        return

    def go_forward(self, p):
        p.forward(3)
        return

    def go_backward(self, p):
        p.backward(3)
        return

    def penup(self, p):
        p.penup()
        return

    def pendown(self, p):
        p.pendown()
        return

    def create_player(self):
        print(f"""⏳ - Creating players...""")
        turtle = tt.Turtle()
        turtle.speed('fastest')
        print(f"""✅ - Player created.""")

    def end_game(self):
        screen = tt.Screen()
        save_as_png(screen.getcanvas(), "result")

    def start_game(self):
        self.create_player
        i = 0
        while True:
            # if keyboard.is_pressed("z"):
            #     self.go_forward(turtle)
            #
            # if keyboard.is_pressed("s"):
            #     self.go_backward(turtle)
            #
            # if keyboard.is_pressed("d"):
            #     self.turn_right(turtle)
            #
            # if keyboard.is_pressed("q"):
            #     self.turn_left(turtle)
            #
            # if keyboard.is_pressed("o"):
            #     self.pendown(turtle)
            #
            # if keyboard.is_pressed("p"):
            #     self.penup(turtle)

            turtle.forward(i * 10)
            turtle.right(144)

            i += 1

            print(f"""{END_PLAYING}""")

            if END_PLAYING == 1:
                self.end_game()
                tt.done()
                tt.Screen().bye()
                break

class Client():
    def __init__(self):
        print(f"""⏳ - Creating a client's instance...️""")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        global OS
        if (os.name == "nt"):
            OS = "W"
            print("You use a Windows system.")
        else:
            OS = "U"
            print("You use a Unix system.")
        print(f"""✅ - Client's instance created.""", end="\n\n")

    def connect(self):
        print(f"""⏳ - Connection to the server...️""")
        try:
            self.client.connect(ADDR)
            print(f"""✅ - Connected to the server.""", end="\n\n")
        except:
            print(f"""❌ - You was not able to connect to the server. Verify the connection parameter...""")
            exit()

    def send(self, msg: str):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def disconnect(self):
        print(f"""⏳ - Sending disconnection request...""")
        self.send(DISCONNECT_MESSAGE)
        print(f"""✅ - Disconnection request sent. \n⏳ - Waiting for a response...️""")
        if self.client.recv(2048).decode(FORMAT) == "leave":
            print(f"""✅ - Response received. You have been disconnected""", end="\n\n")
            exit()

    def select_username(self):
        global MAX_USERNAME_LENGHT
        print(f"""⏳ - Username selection...\n""")
        username_not_found = True
        while username_not_found:
            username = str(input("What username do you want to use?\n\n--> ~"))
            if (" " in username):
                print("You can't have a space in your username. Retry.")
            elif (len(username) == MAX_USERNAME_LENGHT):
                print(f"""Sorry but your username is too long ({len(username)}). The username has to be shorter than {MAX_USERNAME_LENGHT} chars.""")
            else:
                print(f"""Trying to ask if the username {username} is available...""")
                self.send(f"!is-username {username}")
                if (self.client.recv(2048).decode(FORMAT) == "*USERNAME-OK"):
                    self.username = username
                    print(f"""✅ - The username {username} is now your username for this game!""")
                    break

                else:
                    print(f"""❌ - Sorry but the username {username} has been already taken.. Try to find another new one.""")


    def launch_client(self):
        self.select_username()
        print(f"""⏳ - Launching the client...️""")
        first_loop = True
        print(f"""🅿 - Press [ENTER] key to be ready.""")
        input()
        while True:
            if first_loop:
                first_loop = False
                self.send("!ready")
                if (self.client.recv(2048).decode(FORMAT) == "!READY"):
                    print(f"""✅ - You are now ready.\n⏳ - Waiting for others players to be ready...""", end="\n\n")

            if (self.client.recv(2048).decode(FORMAT) == "*START-GAME"):
                self.start_playing()

    def start_playing(self):
        print(f"""⏳ - Starting the game...""")
        p = Player()
        thread = threading.Thread(target=self.start_game)
        thread.start()
        p.start_game()

    def start_game(self):
        print(f"""✅ - Start playing!""")
        self.send("!start-game-ok")
        while True:
            if (self.client.recv(2048).decode(FORMAT) == "*GAME-END"):
                self.end_playing()

    def send_result(self):
        print(f"""⏳ - Asking if we can send the result to the server...""")
        self.send("!sending-result")
        if (self.client.recv(2048).decode(FORMAT) == "*RECEPTION_OK"):
            img_server_port_answeer = self.client.recv(2048).decode(FORMAT)
            if (img_server_port_answeer.startswith("*RECEPTION_PORT")):

                img_scripts_port = img_server_port_answeer[16:]
                print(f"""✅ - Server is waiting for data.""")
                time.sleep(1)
                print(f"""⏳ - Sending the result to the server...""")

                # Launching file to convert and send all the files
                try:
                    if OS == "W":
                        subprocess.run(f"start python3 {IMAGE_SENDER_FILE} -p {img_scripts_port}", shell=True)
                    else:
                        subprocess.run(f"python3 {IMAGE_SENDER_FILE} -p {img_scripts_port}", shell=True)

                except Exception as err:
                    print("Error during sending result the server...")
                    exit()

                print(f"""Result sended to the server({SERVER}).""")
                print(f"""⏳ - Saying to the server that all the image has been sent.""")
                self.send("!stop-sending-result")
                if (self.client.recv(2048).decode(FORMAT) == "*IMAGE_SAVED"):
                    print(f"""✅ - The result has been correctly sent!""")

    def end_playing(self):
        global END_PLAYING
        END_PLAYING = 1
        time.sleep(2)
        print(f"""❌ - End playing!""", end="\n\n")
        print(f"""⏳ - Note time...""")
        self.send_result()
        self.send("!end-game-ok")
        self.disconnect()
        exit()


c = Client()
c.connect()
c.launch_client()