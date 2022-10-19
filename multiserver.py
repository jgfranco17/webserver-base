import argparse
from multiprocessing import Process
from webserver import Server


# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--count", "-c",
                    type=int, required=False, 
                    help="Port to connect to", 
                    default=1)
args = parser.parse_args()


def create_server(host: str, port: int):
    test_server = Server(host=host, port=port)
    test_server.run()
    return test_server


if __name__ == "__main__":
    # Server configuration
    SERVER_IP = "192.168.11.11"
    PORT = 5050

    server_instances = []
    for i in range(args.count):
        instance = Process(target=create_server, args=[SERVER_IP, PORT+i])
        server_instances.append(instance)

    for instance in server_instances:
        instance.start()

    for instance in server_instances:
        instance.join()
