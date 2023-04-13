import socket
import threading
import logging as lg


class Server(object):
    DISCONNECT_MESSAGE = "!DISCONNECT"
    PING_MESSAGE = "!PING"
    HEADER = 64
    MESSAGE_FORMAT = "utf-8"
    
    def __init__(self, host:str=None, port:int=0, name:str="CENTRAL SERVER"):
        # Base properties
        self.__host = host if host is not None else socket.gethostbyname(socket.gethostname())
        self.__port = port
        self.__address = (self.__host, self.__port)
        self.startup_label = f'----- {name} -----'

        # Start up server
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(self.__address)
        self.__host, self.__port = self.__server.getsockname()
        print(f'\n{"*"*len(self.startup_label)}\n{self.startup_label}\n{"*"*len(self.startup_label)}\n')

        # Configure logging
        log_fmt = "[%(levelname)s] %(asctime)s | %(message)s"
        date_fmt = "%H:%M:%S"
        lg.basicConfig(
            level=lg.DEBUG,
            format=log_fmt,
            datefmt=date_fmt
        )

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
        self.__server.listen()
        lg.info(f'[SERVER START] Server {self.__host}:{self.__port} listening!')
        server_running = True
        
        while server_running:
            try:
                conn, addr = self.__server.accept()
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
