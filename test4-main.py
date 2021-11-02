import turtle
import tkinter as TK
import threading
import time
import os

SERVER_FILE = "test4-server.py"

OS = ""
PORT = 0


class Game():
    def __init__(self):
        print(f"Initing the game...")

        #  Detecting the OS
        global OS
        if (os.name == "nt"):
            OS = "W"
            print("You use a Windows system.")
        else:
            OS = "U"
            print("You use a Unix system.")

        print(f"Game inited correctly!")

    def launch_server(self):
        try:
            if OS == "W":
                os.system(f"python3 {SERVER_FILE} -p {PORT}")

            else:
                os.system(f"python3 {SERVER_FILE} -p {PORT}")
                print("Server launched correctly!")

        except:
            print("Error during launching the server...")
            exit()

    def launch(self):
        if (str(input(f"Do you want be an host ? (Y)es or (N)ot: ")).lower() == "y"):
            print("")
            global PORT
            PORT = int(input("Chose a room number! (4 numbers):\n--> #"))
            print(f"Launching the server with room number {PORT}...")
            thread = threading.Thread(target=self.launch_server)
            thread.start()

        else:
            print("You are not a host, you are just launching the game!")


game = Game()
game.launch()