import socket
import threading
import time

PORT = 5084
HEADER = 128
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!leave"
READY_MESSAGE = "!ready"
START_GAME_OK = "!start-game-ok"
END_GAME_OK = "!end-game-ok"
GAME_TIME = 30

READY_COUNT = 0
START_GAME = 0
END_GAME = 0
PLAYERS_CONNECTED = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Server():
    def __init__(self, port):
        print(f"""Creating a server's instance...""")
        self.port = port
        self.addr = socket.gethostbyname(socket.gethostname())
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

    def handle_client(self, conn, addr):
        global START_GAME
        global END_GAME
        global READY_COUNT
        global PLAYERS_CONNECTED
        PLAYERS_CONNECTED.append(conn)
        print(f"{addr} is now connected.", end="\n")


        connected = True
        while connected:
            if (READY_COUNT == (threading.activeCount() - 1) and threading.activeCount() - 1 > 1 and START_GAME == 0):
                self.game_start(conn, addr)

            if (END_GAME == (threading.activeCount() - 1)):
                print(f"""✅ - All players ended the game!""")

            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                if msg == DISCONNECT_MESSAGE:
                    print(f"""{addr} just disconnected.""")
                    conn.send("leave".encode(FORMAT))
                    break
                elif msg == READY_MESSAGE:
                    READY_COUNT += 1
                    print(f"""{addr} is ready, so {READY_COUNT} players are ready.""")
                    conn.send("!READY".encode(FORMAT))
                elif msg == START_GAME_OK:
                    print(f"""{addr} start playing.""")
                    START_GAME += 1
                elif msg == END_GAME_OK:
                    print(f"""{addr} end playing.""")
                    END_GAME += 1
                else:
                    print(f"{addr}$> {msg}")
                    conn.send("!CONNECTED".encode(FORMAT))

        conn.close()

    def game_start(self, conn, addr):
        global START_GAME
        global READY_COUNT
        global END_GAME
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


server = Server(PORT)
server.bind()
server.start()