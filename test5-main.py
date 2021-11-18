import threading
import os
import subprocess
import socket

SERVER_FILE = "test6-server.py"
CLIENT_FILE = "test6-client.py"
LOCAL_IP_ADDR = socket.gethostbyname(socket.gethostname())

IS_HOST = False
SERVER_IP_ADDR = ""
OS = ""
PORT = 0


class Game():
    def __init__(self):
        print("Initing the game...")

        # Detecting the OS
        global OS
        if (os.name == "nt"):
            OS = "W"
            print("You use a Windows system.")
        else:
            OS = "U"
            print("You use a Unix system.")

        print(f"Game inited correctly!")

    def launch_server(self):
        global IS_HOST, SERVER_IP_ADDR
        
        IS_HOST = True
        SERVER_IP_ADDR = LOCAL_IP_ADDR
        
        try:
            if OS == "W":
                subprocess.run(F"start python3 {SERVER_FILE} -p {PORT}", shell=True)
            else:
                subprocess.run(f"nohup python3 {SERVER_FILE} -p {PORT} &", shell=True)

            print("✅ - Server launched correctly!")

        except:
            print("❌ - Error during launching the server...")
            exit()

    def launch_game(self):

        if IS_HOST != True:
            global SERVER_IP_ADDR, PORT

            SERVER_IP_ADDR = input(str("\n\nEnter the server address:\n--> $"))
            PORT = input(str("\n\nEnter the room number:\n--> #"))

        print("Launching client...")
        try:
            if OS == "W":
                subprocess.run(f"start python3 {CLIENT_FILE} -H {SERVER_IP_ADDR} -p {PORT}", shell=True)
            else:
                subprocess.run(f"python3 {CLIENT_FILE} -H {SERVER_IP_ADDR} -p {PORT}", shell=True)

            print("Client launched correctly!")

        except:
            print("Error during launching the server...")
            exit()

    def launch(self):
        if (str(input(f"Do you want be an host ? (Y)es or (N)ot: ")).lower() == "y"):
            print("")
            global PORT
            PORT = int(input("Chose a room number! (4 numbers):\n--> #"))
            print(f"Launching the server with room number {PORT}...")
            self.launch_server()

        else:
            print("You are not a host, you are just launching the game!")

        self.launch_game()

game = Game()
game.launch()