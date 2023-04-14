import pytest
import socket
from webserver.server import Server
from webserver.client import Client


@pytest.fixture(scope='module')
def client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8000))
    yield client
    client.close()
    
    
@pytest.fixture(scope='module')
def server():
    server = Server(host="localhost", port=8000)
    yield server
    server.stop()
