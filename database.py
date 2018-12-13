import socket
import threading

class DatabaseServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.database = {}

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    data = data.decode()
                    data = data[:-1]
                    data = data.split(" ")
                    print(data)
                    if data[0] == 'get':
                        response = self.get_data(data[1])
                    elif data[0] == 'put':
                        response = self.save_data(data[1:])
                    elif data[0] == 'list':
                        response = self.list_data()
                    client.send(response.encode())
                else:
                    raise Exception('Client disconnected')
            except:
                client.close()
                return False

    def save_data(self, data):
        with threading.RLock():
            try:
                self.database[data[0]] = data[1]
                value = "Success\n"
            except KeyError:
                value = "Failed\n"
        return value

    def get_data(self, data):
        with threading.RLock():
            try:
                value = self.database[data] + "\n"
            except KeyError:
                value = "Key not found\n"
        return value

    def list_data(self):
        with threading.RLock():
            try:
                value = ""
                for item, key in self.database.items():
                    value += f"{item}: {key}\n"
            except KeyError:
                value = "Error\n"
        return value


if __name__ == "__main__":
    port_num = 8080
    DatabaseServer('',port_num).listen()
