import socket
import threading
import logging as lg


class Server(object):
    def __init__(self, host:str=None, port:int=0, name:str="CENTRAL SERVER"):
        # Base properties
        self._host = host if host is not None else socket.gethostbyname(socket.gethostname())
        self._port = port
        self._address = (self._host, self._port)

        # Server constants
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.PING_MESSAGE = "!PING"
        self.HEADER = 64
        self.MESSAGE_FORMAT = "utf-8"
        self._STARTUP_LABEL = f'----- {name} -----'

        # Start up server
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind(self._address)
        self._host, self._port = self._server.getsockname()
        print(f'\n{"*"*len(self._STARTUP_LABEL)}\n{self._STARTUP_LABEL}\n{"*"*len(self._STARTUP_LABEL)}\n')

        # Configure logging
        log_fmt = "[%(levelname)s] %(asctime)s | %(message)s"
        date_fmt = "%H:%M:%S"
        lg.basicConfig(
            level=lg.DEBUG,
            format=log_fmt,
            datefmt=date_fmt
        )
        lg.getLogger('matplotlib.font_manager').setLevel(lg.WARNING)

    def handle_client(self, conn, addr) -> None:
        """
        Handles client connections and responses.

        Args:
            conn: Main connection 
            addr: Client address
        """
        client_host, client_port = addr
        lg.info(f'[NEW CONNECTION] Client at {client_host}:{client_port} connected.')
        connected = True

        try:
            while connected:
                message_length = conn.recv(self.HEADER).decode(self.MESSAGE_FORMAT)
                if message_length:
                    show_output = True
                    message_length = int(message_length)
                    message_data = conn.recv(message_length).decode(self.MESSAGE_FORMAT)

                    if message_data == self.DISCONNECT_MESSAGE:
                        connected = False
                        lg.info(f'[NEW DISCONNECTION] Client at {client_host}:{client_port} disconnected!')
                        lg.info(self.__get_active_connections())
                        break

                    if message_data == self.PING_MESSAGE:
                        show_output = False
                    
                    if show_output:
                        host, port = addr
                        lg.info(f'[MESSAGE RECEIVED] {host}:{port} | {message_data}')

                    reply_message = "Message received!"
                    conn.send(reply_message.encode(self.MESSAGE_FORMAT))
        
        except Exception as e:
            lg.warn(f'Error during client handling: {e}')

        finally:
            conn.close()

    @staticmethod
    def __get_active_connections() -> str:
        """
        Gets a count of active threads.
        
        Returns:
            (str): Output message for live connections
        """
        live_connections = threading.activeCount() - 1
        plural = "s" if live_connections > 1 else ""
        return f'[ACTIVE CONNECTIONS] {live_connections} connection{plural}'

    def run(self) -> None:
        """
        Start the server. Uses threading in order to handle
        concurrent responses from multiple clients and prevent
        service clash.
        """
        self._server.listen()
        lg.info(f'[SERVER START] Server {self._host}:{self._port} listening!')
        server_running = True
        
        while server_running:
            try:
                conn, addr = self._server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
                lg.info(self.__get_active_connections())

            except KeyboardInterrupt:
                print("\n")
                lg.warn("[SERVER STOP] Keyboard interrupt detected, stopping server...")
                server_running = False
                break

            except Exception as e:
                lg.warn(f'[SERVER STOP] Error during server handling: {e}')
                server_running = False
                break
        
        print(f'\n******* SERVER STOPPED *******\n')
