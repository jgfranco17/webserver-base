import argparse
from webserver import Client


# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--count", "-c", 
                    type=int, required=False, 
                    help="Number of instances to create", 
                    default=1)
parser.add_argument("--message", "-m", 
                    type=str, required=False, 
                    help="Customize message to be sent to the server", 
                    default="Hello world!")
args = parser.parse_args()


if __name__ == "__main__":
    # Host server config
    SERVER_IP = "192.168.11.11"
    PORT = 5050

    # Client configuration
    test_clients = []
    for i in range(args.count):
        new_client = Client(host=SERVER_IP, port=PORT)
        test_clients.append(new_client)
        new_client.send(args.message)

    for client in test_clients:
        client.send(client.DISCONNECT_MESSAGE)
        