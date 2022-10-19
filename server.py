import argparse
from webserver import Server


# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--server", "-s",
                    type=str, required=False, 
                    help="IP address to listen on", 
                    default="192.168.11.11")
parser.add_argument("--port",
                    type=int, required=False, 
                    help="Port to connect to", 
                    default=5050)
args = parser.parse_args()


if __name__ == "__main__":
    # Server configuration
    SERVER_IP = "192.168.11.11"
    PORT = 5050

    # Run instance
    test_server = Server(host=args.server, port=args.port)
    test_server.run()