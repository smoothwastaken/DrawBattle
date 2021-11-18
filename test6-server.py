import random
import socket
import threading
import time
import argparse
import os
import subprocess
import requests
from bs4 import BeautifulSoup
import json
import netifaces as ni

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
USER_OK_MESSAGE = "!user-ok"
START_RECEIVING_RESULTS = "!sending-result"
STOP_RECEIVING_RESULTS = "!stop-sending-result"
IMAGE_RECV_FILE = "img-sender/server.py"
OS = ""
GAME_TIME = 8
VOTE_TIME = 45
IS_VOTING = 1
NOTES = {}
NOTES_RESULTS = []

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
        ni.ifaddresses('wlan0')
        self.addr = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
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

    def get_theme(self):
        url = "https://www.palabrasaleatorias.com/mots-aleatoires.php"
        reponse = requests.get(url)
        if reponse.ok:
            s = BeautifulSoup(reponse.text, 'html.parser')
            theme = s.find("div", {"style": "font-size:3em; color:#6200C5;"}).get_text()
            self.theme = theme[2:].lower()
            print(theme)

    def start(self):
        print(f"""Starting the listening...""")
        self.s.listen()
        print(f"""Server is listening (address: {self.addr}, port: {self.port})...""", end="\n")
        while True:
            connection, address = self.s.accept()
            thread = threading.Thread(target=self.handle_client, args=(connection, address))
            thread.start()
            print(f"{threading.activeCount() - 1} players connected!", end="\n")

    def start_web_viewer(self):
        print(f"""⏳ - Trying to launch the web viewer...""")
        semaphore = threading.Semaphore(5)
        try:
            with semaphore:
                if OS == "W":
                    subprocess.Popen("cd ./notation-website/ && npm run dev")
                    # subprocess.run(F"cd ./notation-website/ && npm run dev", shell=True)
                else:
                    subprocess.Popen("cd ./notation-website/ && npm run dev")
                    # subprocess.run(f"cd ./notation-website/ && npm run dev", shell=True)

                print("✅ - Web viewer launched correctly!")

        except:
            print("❌ - Error during launching the web viewer :(")
            pass

    def notation_phase1(self, conn):
        print(f"""✅ - Notation phase started""")

        self.start_web_viewer()

        users = ""
        USERNAMES.sort()
        for user in USERNAMES:
            users += f"{user},"
        users = users[:-1]
        
        self.notation_phase2(conn)

    def vote_timer(self):
        global IS_VOTING

        print("sth")

        for user in USERNAMES:
            print(user)
            time.sleep(VOTE_TIME)
            for conn in PLAYERS_CONNECTED:
                try:
                    conn.send(f"*NEXT_PLAYER".encode(FORMAT))
                    print(f"Order sent at: {conn}")
                except:
                    print(f"""Cannot reach the player ({conn}).""")

    def notation_phase2(self, conn):
        global NOTES, NOTES_RESULTS
        USERNAMES_LENGHT = len(USERNAMES)
        USERNAMES.sort()
        for user in USERNAMES:
            NOTES[f"{user}"] = []

        print(NOTES)

        self.vote_timer()

        while IS_VOTING == 1:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                data = conn.recv(msg_length)
                msg = data.decode(FORMAT)

                if msg.startswith("*NOTE"):
                    command = msg.split(" ")
                    user = command[1]
                    note = int(command[2])
                    
                    NOTES[f"{user}"].append(note)

        for user in USERNAMES:
            temp_list = NOTES[f"{user}"]

            j = 0
            for i in temp_list:
                j += i

            m = j / USERNAMES_LENGHT
            
            NOTES_RESULTS.append(m)

        NOTES_RESULTS = NOTES_RESULTS.sort()


        w = ""
        for result in NOTES_RESULTS:
            w += f"{result},"

        w = w[:-1]

        self.conn.send(f"RESULTS {w}".encode(FORMAT))

        print("""LE JEU EST ENFIN FINI, J'ESPÈRE QUE TOUT MARCHE PURÉE""")

    def handle_client_message(self, conn ):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            data = conn.recv(msg_length)
            msg = data.decode(FORMAT)
            return msg

    def handle_img_reception(self, conn, username):
        # try:
        if not os.path.exists(f'./notation-website/results/{username}.png'):
            with open(f'./notation-website/results/{username}.png', 'wb') as f:
                f.write(b'')
        img_scripts_port = random.randint(1500, 9999)
        print(f"""⏳ - Sending port number for the image receiving... (port: {img_scripts_port})""")
        conn.send(f"*RECEPTION_PORT {img_scripts_port}".encode(FORMAT))
        print(f"""✅ - Port sent""")
        if OS == "W":
            subprocess.run(f"start python3 {IMAGE_RECV_FILE} -n {username} -p {img_scripts_port}", shell=True)
        else:
            subprocess.run(f"python3 {IMAGE_RECV_FILE} -n {username} -p {img_scripts_port}", shell=True)

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
                    self.notation_phase1(conn)

                elif msg == USER_OK_MESSAGE:
                    self.notation_phase2(conn)

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

        self.get_theme()

        USERNAMES.sort()

        print(f"""We start the game with {threading.activeCount() - 1} players!""")
        dictionary = {
            "theme": f"{self.theme}",
            "timeToVote": VOTE_TIME,
            "users": USERNAMES,
        }
        with open("./notation-website/dbconfig.json", "w") as outfile:
            outfile.write(json.dumps(dictionary, indent=4))

        print(f"""The theme is: {self.theme.upper()}""")

        users = ""
        for user in USERNAMES:
            users += f"{user},"

        users = users[:-1]

        userss = users.split(",")
        for user in userss:
            print(user)

        for conn in PLAYERS_CONNECTED:
            try:
                conn.send(f"*START-GAME {self.theme} {users} {VOTE_TIME}".encode(FORMAT))
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