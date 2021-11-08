import random
import socket
import threading
import time
import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description="Start a DrawBattle server with arguments.")
parser.add_argument('-p', '--port', metavar="<PORT>", type=int, help="Specify a port number for the creating room.")

args = parser.parse_args()

PORT = args.port
HEADER = 128
IMG_CHUNK_SIZE = 2048
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!leave"
EXIT_CMD = "%stop"
IS_USERNAME_OK = "!is-username"
READY_MESSAGE = "!ready"
START_GAME_OK = "!start-game-ok"
END_GAME_OK = "!end-game-ok"
START_RECEIVING_RESULTS = "!sending-result"
STOP_RECEIVING_RESULTS = "!stop-sending-result"
IMAGE_RECV_FILE = "img-sender/server.py"
OS = ""
GAME_TIME = 10

READY_COUNT = 0
START_GAME = 0
END_GAME = 0
RESULT_PHASE = 0
IN_GAME = 0
USERNAMES = []
PLAYERS_CONNECTED = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Server():
    def __init__(self, port):
        print(f"""Creating a server's instance...""")
        self.port = port
        self.addr = socket.gethostbyname(socket.gethostname())
        # self.addr = "172.20.10.4"
        global OS
        if (os.name == "nt"):
            OS = "W"
            print("OS Detected: Windows system.")
        else:
            OS = "U"
            print("OS Detected: Unix system.")
        print(f"""✅ - Client's instance created.""", end="\n\n")
        print("Host Name is: " + socket.gethostname())
        print("Computer IP Address is: " + self.addr)
        print(f"""Server instance created. (address: {self.addr}, and port {self.port})""", end="\n")

    def bind(self):
        print(f"""Binding the server's infos with a socket...""")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.addr, self.port))
        print(f"""Socket bound.""", end="\n")

    def start(self):
        print(f"""Starting the listening...""")
        self.s.listen()
        print(f"""Server is listening (address: {self.addr}, port: {self.port})...""", end="\n")
        while True:
            connection, address = self.s.accept()
            thread = threading.Thread(target=self.handle_client, args=(connection, address))
            thread.start()
            print(f"{threading.activeCount() - 1} players connected!", end="\n")

    def handle_client_message(self, conn, username, file, ):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            data = conn.recv(msg_length)
            msg = data.decode(FORMAT)
            if msg == STOP_RECEIVING_RESULTS:
                return True
            else:
                return False

    def handle_img_reception(self, conn, username):
        # try:
        if not os.path.exists(f'./results/{username}.png'):
            with open(f'./results/{username}.png', 'wb') as f:
                f.write(b'')
        img_scripts_port = random.randint(1500, 9999)
        print(f"""⏳ - Sending port number for the imagecndjskvnds ({img_scripts_port})""")
        conn.send(f"*RECEPTION_PORT {img_scripts_port}".encode(FORMAT))
        print(f"""✅ - Port sent""")
        if OS == "W":
            subprocess.run(f"start python3 {IMAGE_RECV_FILE} -n {username} -p {img_scripts_port}", shell=True)
        else:
            subprocess.run(f"python3 {IMAGE_RECV_FILE} -n {username} -p {img_scripts_port}", shell=True)

        # except Exception as err:
        #     print(f"Error during receiving results from the client {username}:\n{err}")
        #     exit()


        # file = open(f'./results/{username}.png', "wb")
        # data = conn.recv(IMG_CHUNK_SIZE)
        #
        # i = 0
        # while data:
        #     i += 1
            # try:
            #     print("Try 1")
            #     if self.handle_client_message(conn, username, file):
            #         print("IT WORKS")
            #         file.close()
            #         conn.send("*IMAGE_SAVED".encode(FORMAT))
            #         print(f"""✅ - {username}'s result has been saved!""")
            #         return
            #     else:
            #         print("Not in")
            #         pass
            # except BaseException as err:
            #     print(f"Unexpected {err=}, {type(err)=}")
            #     pass
            # file.write(data)
            # print(i)
            # data = conn.recv(IMG_CHUNK_SIZE)



    def handle_client(self, conn, addr):
        global IS_USERNAME_OK, USERNAMES, START_GAME, END_GAME, IN_GAME, READY_COUNT, PLAYERS_CONNECTED, RESULT_PHASE
        PLAYERS_CONNECTED.append(conn)
        print(f"{addr} is now connected.", end="\n")
        USERNAME = ""

        connected = True
        while connected:
            if (READY_COUNT == (threading.activeCount() - 1) and threading.activeCount() - 1 > 1 and START_GAME == 0):
                self.game_start(conn, addr)

            if (END_GAME == (threading.activeCount() - 1)):
                print(f"""✅ - All players ended the game!""")

            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                data = conn.recv(msg_length)
                msg = data.decode(FORMAT)

                if msg == DISCONNECT_MESSAGE:
                    print(f"""{USERNAME}{addr} just disconnected.""")
                    conn.send("leave".encode(FORMAT))
                    break

                elif msg.startswith(IS_USERNAME_OK):
                    command = msg.split(" ")
                    username = command[1]
                    print(f"""Trying: {username} as username.""")
                    print(username in USERNAMES)
                    if username in USERNAMES:
                        conn.send(f"""*USERNAME-NOT-OK""".encode(FORMAT))
                    else:
                        USERNAME = username
                        USERNAMES.append(username)
                        conn.send(f"""*USERNAME-OK""".encode(FORMAT))

                elif msg == (START_RECEIVING_RESULTS):
                    conn.send("*RECEPTION_OK".encode(FORMAT))
                    self.handle_img_reception(conn, username)

                elif msg == READY_MESSAGE:
                    READY_COUNT += 1
                    IN_GAME += 1
                    print(f"""{USERNAME}{addr} is ready, so {READY_COUNT} players are ready.""")
                    conn.send("!READY".encode(FORMAT))

                elif msg == START_GAME_OK:
                    print(f"""{USERNAME}{addr} start playing.""")
                    START_GAME += 1

                elif msg == END_GAME_OK:
                    print(f"""{USERNAME}{addr} end playing.""")
                    END_GAME += 1

                elif msg == EXIT_CMD:
                    conn.close()
                    self.s.close()
                    exit()


                else:
                    print(f"{USERNAME}({addr})$> {msg}")
                    conn.send("!CONNECTED".encode(FORMAT))

        conn.close()

    def game_start(self, conn, addr):
        global START_GAME, READY_COUNT, END_GAME, RESULT_PHASE
        START_GAME = 1

        print(f"""We start the game with {threading.activeCount() - 1} players!""")
        for conn in PLAYERS_CONNECTED:
            try:
                conn.send("*START-GAME".encode(FORMAT))
            except:
                print(f"""Cannot reach the player ({conn}).""")
        time.sleep(GAME_TIME)
        print(f"""Ending the game""")
        for conn in PLAYERS_CONNECTED:
            conn.send("*GAME-END".encode(FORMAT))
            READY_COUNT -= 1
            START_GAME -= 1
            END_GAME -= 1

        print(f"""Result phase""")


server = Server(PORT)
server.bind()
server.start()