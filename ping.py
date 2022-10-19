import argparse
from webserver import Client


class PingService(object):
    def __init__(self, target, port):
        self._target = target
        self._port = port
        self._clientbase = Client(host=target, port=port)

    def run(self):
        print(f'Running ping @ target {self._target}:{self._port}')
        self._clientbase.ping(plot_data=True)
        print("Connection closed.")


if __name__ == "__main__":
    """
    Sample usage:

    'python ping.py -s 192.168.0.90 -p 5050'
    pings 192.168.0.90:5050 until stopped
    """
    # Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", "-s", 
                        type=str, required=False, 
                        help="Server host to connect to", 
                        default="0.0.0.0")
    parser.add_argument("--port", "-p", 
                        type=int, required=False, 
                        help="Server port to connect to", 
                        default=5050)
    args = parser.parse_args()

    # Client configuration
    pingbot = PingService(target=args.server, port=args.port)
    pingbot.run()
        