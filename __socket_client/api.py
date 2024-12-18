import socket
import json
from .logger import log

#INFO: The "log" function is a utillity function for logging. The "INFO" logs are the responses and the "DEBUG" logs are for debuging

class SocketClient:
    def __init__(self, client_name="Amirreza Yarahmadi CLIENT", server_ip="0.0.0.0", server_port=8000):
        self.client_name = client_name
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, client_number):
        try:
            # Trying to connect to the server
            self.client_socket.connect((self.server_ip, self.server_port))
            log(f"Connected to server at {self.server_ip}:{self.server_port}", level="DEBUG", source="SocketClient", function="send_message")
            
            # Sending the "client name" and the "desired int" to the server
            log(f"Sending message to the server", level="DEBUG", source="SocketClient", function="send_message")
            message = {"client_name": self.client_name, "client_number": client_number}
            self.client_socket.send(json.dumps(message).encode())
            
            # If the value is out of range the server should be terminated
            if not (1 <= client_number <= 100):
                log("The integer input out of range. Terminating the server", level="WARNING", source="SocketClient", function="send_message")
                
                # Terminating the client after sending the termination call
                # self.client_socket.close()
                exit()
            
            # Loading the server response
            log(f"Recieved message from server", level="DEBUG", source="SocketClient", function="send_message")
            response = json.loads(self.client_socket.recv(1024).decode())
            server_name = response["server_name"]
            server_number = response["server_number"]
            
            # logging the server response
            log(f"Client Name: {self.client_name} | Server Name: {server_name}", level="INFO", source="SocketClient", function="send_message")
            log(f"Client Number: {client_number} | Server Number: {server_number} | Sum: {client_number + server_number}", level="INFO", source="SocketClient", function="send_message")
        except Exception as e:
            # Exception for handling errors and logging
            log(f"Error connecting to server: {e}", level="ERROR", source="SocketClient", function="send_message")
        finally:
            # Terminating the client afterward
            self.client_socket.close()