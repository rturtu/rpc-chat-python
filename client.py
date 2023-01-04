import threading
import grpc
import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

url = 'localhost'
port = 11912

class Client:

    def __init__(self):
        print("Enter username: ")
        username = input()
        self.username = username
        channel = grpc.insecure_channel(f"{url}:{str(port)}")
        self.conn = rpc.ChatServerStub(channel)
        print(f"Client started as {username}");
        threading.Thread(target=self.message_listener, daemon=True).start()


    def message_listener(self):
        chat_auth = chat.ChatStreamAuth()
        chat_auth.name = self.username
        for message in self.conn.ChatStream(chat_auth):
            print(f"\n{message.name}: {message.message}")

    def send_message(self, message):
        new_message = chat.Message()
        new_message.name = self.username
        new_message.message = message
        # print(f"[Client] sending message {message}")
        self.conn.SendMessage(new_message)

    def prompt(self):
        while True:
            message = input(f"[{self.username}]: ")
            if message == '':
                continue
            c.send_message(message)



if __name__ == '__main__':
    c = Client()
    c.prompt()
