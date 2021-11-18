import http.server
import socketserver
import socket
import argparse
from time import gmtime


parser = argparse.ArgumentParser(description="Start a DrawBattle server with arguments.")
parser.add_argument('-p', '--port', metavar="<PORT>", type=int, help="Specify a port number for the creating room.")

args = parser.parse_args()

PORT = args.port
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer((socket.gethostbyname(socket.gethostname()), PORT), Handler) as httpd:
    print(f"""Web server launched on port {PORT}.""")
    httpd.serve_forever()
