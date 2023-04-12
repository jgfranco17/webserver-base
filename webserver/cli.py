"""
CLI interface for webserver project.
"""
import argparse
from .server import Server
from .client import Client


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m project_template` and `$ project_template `.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", "-m",
                        type=str, required=True,
                        help="Set to server or client behavior")
    parser.add_argument("--address", "-a",
                        type=str, required=True,
                        help="Host IP to bind to")
    parser.add_argument("--port", "-p",
                        type=str, required=True,
                        help="Target port to bind to")
    args = parser.parse_args()
    
    mode = args.mode.lower()
    if mode not in ("server", "client"):
        raise ValueError(f'Invalid mode: \"{mode}\" not recognized.')
    
    print(f'Running webserver in {mode} mode.')
    if mode == "server":
        server = Server(host=args.address, port=args.port)
        server.run()
