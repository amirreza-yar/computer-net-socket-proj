import socket
import random
import json
import threading
from .logger import log

#INFO: The "log" function is a utillity function for logging. The "INFO" logs are the responses and the "DEBUG" logs are for debuging

class SocketServer:
    def __init__(self, server_name="Amirreza Yarahmadi CLIENT", server_ip="0.0.0.0", server_port=8000):
        self.server_name = server_name
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_running = True
            
    def start_server(self):
        # Starting the server and binding with the default gateway of computer and the desired port
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)
        log(f"{self.server_name} started and listening on {self.server_ip}:{self.server_port}", level="INFO", source="SocketServer", function="start_server")
        
        while self.server_running: # The "self.server_running" val indicate the server running
            try:
                self.server_socket.settimeout(1) # The socket timeout, so that other proccesses run properly (ex. checking the "self.server_running", terminating the server)
                client_socket, addr = self.server_socket.accept()
                log(f"Connection accepted from {addr}", level="DEBUG", source="SocketServer", function="start_server")
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except socket.timeout:
                continue
            except Exception as e:
                # log(f"Error in server loop: {e}", level="ERROR", source="SocketServer", function="start_server")
                break

    def handle_client(self, client_socket):
        # Handling the client messages
        try:
            # Loading "cliend name" and its "chosen int"
            message = json.loads(client_socket.recv(1024).decode())
            client_name = message["client_name"]
            client_number = message["client_number"]
            log(f"Message recieved from client", level="DEBUG", source="SocketServer", function="handle_client")
            
            # If the client's "chosen int" is out of range, the server should be terminated
            if not (1 <= client_number <= 100):
                log(f"Client int out of range: {client_number}. Terminating the server.", level="WARNING", source="SocketServer", function="handle_client")
                
                # Closing the client connection and terminating the server
                client_socket.close()
                log(f"Client connection closed", level="DEBUG", source="SocketServer", function="handle_client")
                self.server_running = False
                self.server_socket.close()
                exit()

            # Choosing a random int as the "server int"
            server_number = random.randint(1, 100)
            log(f"Client Name: {client_name} | Server Name: {self.server_name}", level="INFO", source="SocketServer", function="handle_client")
            log(f"Client Number: {client_number} | Server Number: {server_number} | Sum: {client_number + server_number}", level="INFO", source="SocketServer", function="handle_client")
            
            # Sending the "server name" and "server int" as response
            log(f"Sending client response", level="DEBUG", source="SocketServer", function="handle_client")
            response = {"server_name": self.server_name, "server_number": server_number}
            client_socket.send(json.dumps(response).encode())
        except Exception as e:
            # Logging the errors
            log(f"Error handling client: {e}", level="ERROR", source="SocketServer", function="handle_client")
        finally:
            # Closing client connection afterward
            client_socket.close()