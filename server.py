from concurrent import futures
import grpc
import chat_pb2 as chat
import chat_pb2_grpc as rpc
import time

class Server(rpc.ChatServerServicer):

    def __init__(self):
        self.messages_dict = {}
        print("[Server] Server started")


    def ChatStream(self, request: chat.ChatStreamAuth, context):
        print(f"[Server] New Chat listener {request.name}")
        chat_user = request.name
        self.messages_dict[chat_user] = []
        message_index = 0
        while True:
            while len(self.messages_dict[chat_user]) > message_index:
                message_to_send = self.messages_dict[chat_user][message_index]
                message_index = message_index + 1
                print(f"Sending {message_to_send.name} {message_to_send.message}")
                yield message_to_send

    def SendMessage(self, request: chat.Message, context):
        print(f"[Server] {request.name}: {request.message}")
        # You can add request.name and request.message in the Database here
        # self.messages.append(request);
        return chat.Empty()

    def prompt(self):
        # This is the input message interface
        while True:
            message = input()
            if message == '':
                continue
            if message[0] == '/':
                split_message = message[1:].split(' ')
                receiver = split_message[0]
                message = " ".join(split_message[1:])
                new_message = chat.Message()
                new_message.name = "Admin"
                new_message.message = message
                if receiver in self.messages_dict:
                    self.messages_dict[receiver].append(new_message)
            else:
                new_message = chat.Message()
                new_message.name = "Admin"
                new_message.message = message
                for key in self.messages_dict:
                    self.messages_dict[key].append(new_message)


if __name__ == '__main__':
    port = 11912
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_server = Server()
    rpc.add_ChatServerServicer_to_server(chat_server, server)
    server.add_insecure_port("[::]:" + str(port))
    server.start()

    chat_server.prompt()
