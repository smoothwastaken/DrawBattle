import socket
import threading
import turtle as tt
import keyboard
import os
import argparse
import time
import subprocess
import webbrowser
import sys

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

NOTES = {}

VOTE_COMPLETE = 0

END_PLAYING = 0

turtle = tt.Turtle()


def save_as_png(canvas, fileName):
    # save postscipt image
    print(f"""⏳ - Saving the Tkinter's canvas as .eps file...""")
    canvas.postscript(file=fileName + '.eps')
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

    def go_forward(self):
        self.turtle.forward(3)

    def go_backward(self):
        self.turtle.backward(3)

    def turn_right(self):
        self.turtle.right(10)

    def turn_left(self):
        self.turtle.left(10)

    def pen_is_up(self):
        self.turtle.penup()

    def pen_is_down(self):
        self.turtle.pendown()

    def pen_10(self):
        self.turtle.pensize(10)

    def pen_9(self):
        self.turtle.pensize(9)

    def pen_8(self):
        self.turtle.pensize(8)

    def pen_7(self):
        self.turtle.pensize(7)

    def pen_6(self):
        self.turtle.pensize(6)

    def pen_5(self):
        self.turtle.pensize(5)

    def pen_4(self):
        self.turtle.pensize(4)

    def pen_3(self):
        self.turtle.pensize(3)

    def pen_2(self):
        self.turtle.pensize(2)

    def pen_1(self):
        self.turtle.pensize(1)

    def clear_screen(self):
        self.turtle.clear()

    def fill_start(self):
        self.turtle.begin_fill()

    def fill_end(self):
        self.turtle.end_fill()

    def color_blue(self):
        self.turtle.pencolor("blue")

    def color_red(self):
        self.turtle.pencolor("red")

    def color_yellow(self):
        self.turtle.pencolor("yellow")

    def color_green(self):
        self.turtle.pencolor("green")

    def color_orange(self):
        self.turtle.pencolor("orange")

    def color_pink(self):
        self.turtle.pencolor("pink")

    def color_brown(self):
        self.turtle.pencolor("brown")

    def color_purple(self):
        self.turtle.pencolor("purple")

    def color_black(self):
        self.turtle.pencolor("black")

    def color_cyan(self):
        self.turtle.pencolor("cyan")

    def color_white(self):
        self.turtle.pencolor("white")

    def create_player(self):
        print(f"""⏳ - Creating players...""")
        self.turtle = tt.Turtle()
        self.set_title()
        self.screen = tt.Screen()
        self.screen.bgcolor("beige")
        turtle.speed('fastest')
        print(f"""✅ - Player created.""")

    def set_title(self):
        tt.title(f"Thème: {self.theme}")

    def end_game(self):
        screen = tt.Screen()
        save_as_png(screen.getcanvas(), "result")
        screen.bye()

    def start_game(self, theme):
        self.theme = theme
        self.create_player
        self.set_title()

        self.screen.setup(1280, 1080)
        self.screen.bgcolor("beige")

        while True:
            if keyboard.is_pressed("z"):
                self.go_forward()

            if keyboard.is_pressed("esc"):
                break

            if keyboard.is_pressed("s"):
                self.go_backward()

            if keyboard.is_pressed("q"):
                self.turn_left()

            if keyboard.is_pressed("d"):
                self.turn_right()

            if keyboard.is_pressed("f"):
                self.pen_is_up()

            if keyboard.is_pressed("e"):
                self.pen_is_down()

            if keyboard.is_pressed("0"):
                self.pen_10()

            if keyboard.is_pressed("9"):
                self.pen_9()

            if keyboard.is_pressed("8"):
                self.pen_8()

            if keyboard.is_pressed("7"):
                self.pen_7()

            if keyboard.is_pressed("6"):
                self.pen_6()

            if keyboard.is_pressed("5"):
                self.pen_5()

            if keyboard.is_pressed("4"):
                self.pen_4()

            if keyboard.is_pressed("3"):
                self.pen_3()

            if keyboard.is_pressed("2"):
                self.pen_2()

            if keyboard.is_pressed("1"):
                self.pen_1()

            if keyboard.is_pressed(" "):
                self.clear_screen()

            if keyboard.is_pressed("+"):
                self.fill_start()

            if keyboard.is_pressed("-"):
                self.fill_end()

            if keyboard.is_pressed("!"):
                self.color_black()

            if keyboard.is_pressed("x"):
                self.color_red()

            if keyboard.is_pressed("c"):
                self.color_yellow()

            if keyboard.is_pressed("v"):
                self.color_green()

            if keyboard.is_pressed("b"):
                self.color_orange()

            if keyboard.is_pressed("n"):
                self.color_pink()

            if keyboard.is_pressed(","):
                self.color_purple()

            if keyboard.is_pressed(";"):
                self.color_brown()

            if keyboard.is_pressed(":"):
                self.color_blue()

            if keyboard.is_pressed("w"):
                self.color_cyan()

            if keyboard.is_pressed("<"):
                self.color_white()

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
                print(
                    f"""Sorry but your username is too long ({len(username)}). The username has to be shorter than {MAX_USERNAME_LENGHT} chars.""")
            else:
                print(f"""Trying to ask if the username {username} is available...""")
                self.send(f"!is-username {username}")
                if (self.client.recv(2048).decode(FORMAT) == "*USERNAME-OK"):
                    self.username = username
                    print(f"""✅ - The username {username} is now your username for this game!""")
                    break

                else:
                    print(
                        f"""❌ - Sorry but the username {username} has been already taken.. Try to find another new one.""")

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

            recved = self.client.recv(2048).decode(FORMAT)
            if (recved.startswith("*START-GAME")):
                command = recved.split(" ")
                self.theme = command[1]
                users = command[2]
                self.users = users.split(",")
                self.vote_time = int(command[3])
                self.start_playing()

    def start_playing(self):
        global NOTES
        print(f"""⏳ - Starting the game...""")
        print(f"""✅ - The theme is: {self.theme}""")
        for user in self.users:
            NOTES[f"{user}"] = []

        print(NOTES)
        p = Player()
        thread = threading.Thread(target=self.start_game)
        thread.start()
        p.start_game(theme=self.theme)

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
                # if (self.client.recv(2048).decode(FORMAT) == "*IMAGE_SAVED"):
                #     print(f"""✅ - The result has been correctly sent!""")

    # def note_timer(self):
    #     global VOTE_TIME, VOTE_COMPLETE
    #     timer = VOTE_TIME
    #     for user in self.users:
    #         timer = VOTE_TIME
    #         VOTE_COMPLETE
    #         print(f"Les votes commencent pour: {user}, vous avez {VOTE_TIME} secondes ! (pas de mauvaise foi bien sûr...)")
    #
    #         while timer != -1:
    #             print(f"Temp restant pour voter pour {user}...")
    #             timer -= 1
    #             time.sleep(1)
    #
    #         VOTE_COMPLETE = 1
    #         print("Joueur suivant")

    # def note_timer(self):
    #     global VOTE_TIME, VOTE_COMPLETE
    #     timer = VOTE_TIME
    #     for user in self.users:
    #         time.sleep(timer)
    #         VOTE_COMPLETE = 1
    #         time.sleep(1)

    # def set_time(self):
    #     global VOTE_COMPLETE
    #     VOTE_COMPLETE = 1
    #     time.sleep(1)
    #     VOTE_COMPLETE = 0

    # def input_with_timeout(self, prompt, timeout):
    #     sys.stdout.write(prompt)
    #     sys.stdout.flush()
    #     ready, _, _ = select.select([sys.stdin], [], [], timeout)
    #     if ready:
    #         return sys.stdin.readline().rstrip('\n')  # expect stdin to be line-buffered
    #
    #     print("Timer's end")
    #     raise TimeoutError

    # def note_timer(self):
    #     global VOTE_COMPLETE
    #
    #     for user in self.users:
    #         while True:
    #             if (self.client.recv(2048).decode(FORMAT) == "*NEXT_PLAYER"):
    #                 VOTE_COMPLETE = 1
    #                 time.sleep(1)
    #                 break

    # def alarm_handler(self, signum, frame):
    #     raise TimeoutError

    # def input_with_timeout(self, prompt, timeout):
    # set signal handler
    # signal.signal(signal.SIGALRM, self.alarm_handler)
    # signal.alarm(timeout)  # produce SIGALRM in `timeout` seconds
    #
    # try:
    #     return input(prompt)
    # finally:
    #     signal.alarm(0)

        # global VOTE_COMPLETE, NOTES
        #
        # for user in self.users:
        #     note = 5
        #     note = input(f"Donne une note à {user} (entre 0 et 10 compris) !\n--> *")
        #
        #     print(note)
        #
        #     if type(note) != int:
        #         print("Tu n'as pas donné une note correcte, entre un nombre pile entre 0 et 10 compris")
        #
        #     elif note < 0:
        #         print(f"{note} est trop basse pour être donner (comment t'es méchant)..")
        #
        #     elif note > 10:
        #         print(f"On sait que vous êtes pote mais {note} quand même c'est beaucoup..")
        #
        #     else:
        #         print(f"Tu as donné la note {note} à {user} !")
        #         NOTES[f"{user}"].append(note)
        #         print(NOTES)
        #         break
        #
        #     print("Attente de vote pour le joueur suivant...")
        #
        #     if (self.client.recv(2048).decode(FORMAT) == "*NEXT_PLAYER"):
        #         print("Joueur suivant!\n\n")
        #         pass

    def input_mod(self, prompt):
        sys.stdout.write(prompt)
        sys.stdout.flush()
        return sys.stdin.readline().rstrip('\n')

    def notation_phase1(self, n):
        note = 5
        note = self.input_mod(f"Donne une note à {self.users[n]} (entre 0 et 10 compris) !\n--> *")

        print(note)

        print(f"Tu as donné la note {note} à {self.users[n]} !")
        NOTES[f"{self.users[n]}"].append(note)
        print(NOTES)

        print("Attente de vote pour le joueur suivant...")

        while True:
            if (self.client.recv(2048).decode(FORMAT) == "*NEXT_PLAYER"):
                print("Joueur suivant!\n\n")
                break

    def notation_phase(self):
        self.notation_phase1(n=0)
        self.notation_phase1(n=1)
        self.notation_phase1(n=2)
        self.notation_phase1(n=3)


    def end_playing(self):
        global END_PLAYING
        END_PLAYING = 1
        time.sleep(2)
        print(f"""❌ - End playing!""", end="\n\n")
        print(f"""⏳ - Note time...""")
        # Send results
        self.send_result()
        print("⏳ - Opening the compositions web-viewer...")
        # Start webserver for a delay
        time.sleep(2)
        webbrowser.open(f"http://{SERVER}:3000")

        self.notation_phase()

        # Game ends
        self.send("!end-game-ok")
        self.disconnect()
        exit()


c = Client()
c.connect()
c.launch_client()