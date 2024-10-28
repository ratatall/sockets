import socket

def start_client(host='localhost', port=12345):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    while True:
        command = input("Enter command (POST, GET, DELETE, QUIT): ").strip().upper()
        if command == "QUIT":
            client.send(command.encode())
            response = client.recv(1024).decode()
            print(response)
            break
        elif command == "POST":
            client.send(command.encode())
            message_lines = []
            while True:
                line = input()
                if line == "#":
                    break
                message_lines.append(line)
            client.send("\n".join(message_lines).encode())
            client.send(b"#")  # End of message
            response = client.recv(1024).decode()
            print(response)
        elif command == "GET":
            client.send(command.encode())
            response = client.recv(4096).decode()
            print("Happy Socket Programming")
            print("Messages:\n" + response)
        elif command == "DELETE":
            client.send(command.encode())
            msg_ids = []
            while True:
                line = input("Enter message ID to delete (or # to finish): ")
                if line == "#":
                    break
                msg_ids.append(line)
            client.send("\n".join(msg_ids).encode())
            client.send(b"#")  # End of delete operation
            response = client.recv(1024).decode()
            print(response)
        else:
            print("ERROR - Command not understand")

    client.close()

if __name__ == "__main__":
    start_client()