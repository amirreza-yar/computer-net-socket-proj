from __socket_client.api import SocketClient

if __name__ == "__main__":
    client = SocketClient("Amirreza Yarahmadi Client", server_port=8000)
    client_number = int(input("Enter an integer between 1 and 100: "))
    client.send_message(client_number)