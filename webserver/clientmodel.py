import socket
import numpy as np
import logging as lg
import datetime as dt
import matplotlib.pyplot as plt
from os import getcwd
from time import time, sleep, perf_counter_ns
from .timing import TimeInterval


class Client(object):
    DISCONNECT_MESSAGE = "!DISCONNECT"
    PING_MESSAGE = "!PING"
    HEADER = 64
    MESSAGE_FORMAT = "utf-8"
    MAX_RESPONSE_SIZE = 1024
    
    def __init__(self, host, port):
        # Base properties
        self._host = host
        self._port = port
        self._address = (self._host, self._port)

        # Configure logging
        log_fmt = "[%(levelname)s] %(asctime)s | %(message)s"
        date_fmt = "%H:%M:%S"
        lg.basicConfig(
            level=lg.DEBUG,
            format=log_fmt,
            datefmt=date_fmt
        )
        lg.getLogger('matplotlib.font_manager').setLevel(lg.WARNING)

        # Create client instance
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(self._address)
        lg.info(f'[CLIENT] Connected to {self._host}:{self._port}')

    @staticmethod
    def __output_data(dataset:list) -> None:
        """
        Writes the gathered data into an external file.

        Args:
            dataset (list): Data points to be written to the output file
        """
        with open(f'{getcwd()}/output.txt', "w+") as file:
            current_time = dt.datetime.now().strftime("%d %B %Y, %I:%M:%S %p")
            file.write(f'{current_time}\n')
            for data in dataset:
                file.write(f'{data}\n')
        
        lg.info("Data exported to file.")

    @staticmethod
    def __plot_data(dataset:list) -> None:
        """
        Plots the gathered data to a line graph.

        Args:
            dataset (list): List of latencies to be plotted
        """
        try:
            # Set up data
            x_data = np.array([i+1 for i in range(len(dataset))], dtype=np.float64)
            y_data = np.array(dataset, dtype=np.float64)

            # Generate plot
            plot_title = f'Latency Plot ({len(dataset)//60} minutes)'
            plot_color = "firebrick"
            plt.plot(x_data, y_data, color=plot_color)
            plt.axhline(y=np.average(y_data), color="goldenrod", linestyle=":")  
            plt.title(plot_title)
            plt.xlim(0, np.max(x_data))
            plt.ylim(0, np.max(y_data))
            plt.xlabel("Time (s)")
            plt.ylabel("Latency (ms)")
            plt.grid()
            plt.show()
            lg.info("Results plotted to graph.")
        
        except Exception as e:
            lg.warn(f'Error while plotting results: {e}')

    def send(self, msg) -> None:
        """
        Send a message from the client to the server.

        Args:
            msg (str): Message to be sent to the server
        """
        # Encoding of primary message
        try:
            message = msg.encode(self.MESSAGE_FORMAT)
            message_length = len(message)
            send_length = str(message_length).encode(self.MESSAGE_FORMAT)
            send_length += b" " * (self.HEADER - len(send_length))

            # Use time.perf_counter_ns() to determine latency
            start_time_ns, end_time_ns = 0, 0
            self._client.send(send_length)
            start_time_ns = perf_counter_ns()
            self._client.send(message)
            response = self._client.recv(self.MAX_RESPONSE_SIZE)
            end_time_ns = perf_counter_ns()

            # Don't compute latency if the message is a disconnect request
            if msg != self.DISCONNECT_MESSAGE:
                rtt_ms = (end_time_ns - start_time_ns) / 1_000_000  # convert to milliseconds
                print(f'Latency: {rtt_ms:.3f} ms')

        except Exception as e:
            lg.warn(f'Error during client communication: {e}')

    def ping(self, save_data:bool=False, plot_data:bool=False):
        """
        Ping the server repeatedly.
        """
        try:
            # Configure ping message for sending
            message = self.PING_MESSAGE.encode(self.MESSAGE_FORMAT)
            message_length = len(message)
            send_length = str(message_length).encode(self.MESSAGE_FORMAT)
            send_length += b" " * (self.HEADER - len(send_length))

            # Ping server in intervals
            recorded_rtt_data = []
            is_pinging = True
            ping_start_time = time()
            while is_pinging:
                try:
                    now = dt.datetime.now().strftime("%H:%M:%S")
                    start_time_ns, end_time_ns = 0, 0
                    self._client.send(send_length)
                    start_time_ns = perf_counter_ns()
                    self._client.send(message)
                    response = self._client.recv(self.MAX_RESPONSE_SIZE)
                    end_time_ns = perf_counter_ns()
                    rtt_ms = (end_time_ns - start_time_ns) / 1_000_000  # convert ns to ms
                    print(f'[{now}] Latency: {rtt_ms:.3f} ms')
                    recorded_rtt_data.append(rtt_ms)
                    sleep(1)

                except KeyboardInterrupt:
                    print("\n")
                    lg.info("[CLIENT PING STOP] Stopping ping.")
                    is_pinging = False
                    break

            # Prepare data summary
            ping_end_time = time()
            duration = ping_end_time - ping_start_time
            runtime = TimeInterval.from_time_diff(duration)
            refined_data = np.array(recorded_rtt_data, dtype=np.float64)
            min_ping, max_ping = np.min(refined_data), np.max(refined_data)
            avg_ping = np.average(refined_data)
            print("\n******* PING DATA *******")
            print(f'Duration: {runtime}')
            print(f'Average latency: {avg_ping:.3f} ms')
            print(f'Minimum ping: {min_ping:.3f} ms')
            print(f'Maximum ping: {max_ping:.3f} ms')

            if save_data:
                self.__output_data(recorded_rtt_data)

            if plot_data:
                self.__plot_data(recorded_rtt_data)

        except Exception as e:            
            lg.warn(f'Error during ping routine: {e}')

        finally:
            # Ensures disconnection at the end of run
            self.send(self.DISCONNECT_MESSAGE)
