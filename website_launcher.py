#!/bin/python3
import os
import subprocess

OS = ""


class Launcher():
    def __init__(self):
        global OS
        if (os.name == "nt"):
            OS = "W"
            print("OS Detected: Windows system.")
        else:
            OS = "U"
            print("OS Detected: Unix system.")

    def launch(self):
        try:
            if OS == "W":
                subprocess.run(f"cd notation-website && npm run dev", shell=True)
            else:
                subprocess.run(f"cd ./notation-website && npm run dev", shell=True)

        except Exception as err:
            print("Error during launching the preview website...")
            exit()


l = Launcher()
l.launch()
