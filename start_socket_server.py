from __socket_server.api import SocketServer

if __name__ == "__main__":
    socket_server = SocketServer("Amirreza Yarahmadi Server", server_port=8000)
    # threading.Thread(target=server.start_server, daemon=True).start()
    socket_server.start_server()