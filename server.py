import socket
import argparse
from webserver import Server


# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--server", "-s",
                    type=str, required=False, 
                    help="IP address to listen on", 
                    default=socket.gethostbyname(socket.gethostname()))
parser.add_argument("--port",
                    type=int, required=False, 
                    help="Port to connect to", 
                    default=0)
args = parser.parse_args()


if __name__ == "__main__":
    # Run instance
    test_server = Server(host=args.server, port=args.port)
    test_server.run()