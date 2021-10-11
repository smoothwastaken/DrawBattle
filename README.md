# NSI-PROJECT-DrawBattle
## **Introduction**
  DrawBattle is a NSI Project where we have to make something with the python module:

> [`turtle`](https://docs.python.org/3/library/turtle.html#module-turtle "turtle: An educational framework for simple graphics applications")  — Turtle graphics

Here's the development branch got update each time I work on.
I hope that you will get fun to see how far we gone! 
 
 Have a nice day :)

## How to use
The use if very simple.
To start playing, you have to launch the server on an available port (see it as a room number) with the following command:
### Linux

    sudo python3 server.py
### Windows

    python2 server.py

 Be sure that the players are on the same network than you. 
After it you can just start playing as a player with the following command:
### Linux

    sudo python3 client.py
### Windows

    python2 client.py

See the "Issues" section to know why MacOs isn't supported.


## Issues

### MacOS players
For the players movements, we used keyboard module:

    import keyboard

But the issue is that with macOs, this python module crash all the things because of this function:

    keyboard.is_pressed("key")
So I needed to test on others computers. And as you can understand, if you want to play on a computer with MacOs on you can't because of this module. If there is any fix I'll update the repository. 
