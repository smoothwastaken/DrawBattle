import socket
import threading
import turtle as tt
# import keyboard
import time
from PIL import Image

PORT = 5084
HEADER = 128
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!leave"
SERVER = "127.0.0.1"
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

    # def turn_right(self, p):
    #     p.right(5)
    #     return
    #
    # def turn_left(self, p):
    #     p.left(5)
    #     return
    #
    # def go_forward(self, p):
    #     p.forward(3)
    #     return
    #
    # def go_backward(self, p):
    #     p.backward(3)
    #     return
    #
    # def penup(self, p):
    #     p.penup()
    #     return
    #
    # def pendown(self, p):
    #     p.pendown()
    #     return

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

            turtle.forward(i * 20)
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

    def launch_client(self):
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

    def end_playing(self):
        global END_PLAYING
        END_PLAYING = 1
        print(f"""❌ - End playing!""", end="\n\n")
        time.sleep(2)
        self.send("!end-game-ok")
        self.disconnect()
        exit()


c = Client()
c.connect()
c.launch_client()