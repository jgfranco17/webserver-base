import pytest
from .conftest import server, client


def test_connection(client):
    assert client.fileno() > 0


def test_send_message(client):
    message = b'Hello, world!'
    client.sendall(message)
    assert client.recv(1024) == message


def test_invalid_message(client):
    with pytest.raises(ValueError):
        client.sendall(None)


def test_disconnect(client):
    assert client.fileno() > 0
    client.close()
    assert client.fileno() < 0
