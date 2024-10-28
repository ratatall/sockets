import socket
import threading
import time

# Store messages with their IDs and timestamps
messages = {}
message_id = 0

def handle_client(client_socket):
    global message_id
    while True:
        command = client_socket.recv(1024).decode().strip()
        if command == "QUIT":
            client_socket.send(b"OK")
            break
        elif command == "POST":
            msg_lines = []
            while True:
                line = client_socket.recv(1024).decode().strip()
                if line == "#":
                    break
                msg_lines.append(line)
            message_content = "\n".join(msg_lines)
            messages[message_id] = (message_content, time.ctime())
            client_socket.send(b"OK")
            message_id += 1
        elif command == "GET":
            if not messages:
                response = "No messages available."
            else:
                response = "\n".join(
                    [f"{id}: {msg[0]} (Received at {msg[1]})" for id, msg in messages.items()]
                )
                client_socket.send(response.encode())
        elif command == "DELETE":
            errors = []
            while True:
                msg_id = client_socket.recv(1024).decode().strip()
                if line == "#":
                    break
                if msg_id.isdigit() and int(msg_id) in messages:
                    del messages[int(msg_id)]
                else:
                    errors.append(msg_id)
            
            #for msg_id in msg_ids:
                #if msg_id.isdigit() and int(msg_id) in messages:
                    #del messages[int(msg_id)]
                #else:
                    #print("ERROR - Wrong ID")
                    #errors.append(msg_id)
            if errors:
                client_socket.send(b"ERROR - Wrong ID")
            else:
                client_socket.send(b"OK")

    client_socket.close()

def start_server(host='localhost', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    
    while True:
        client_sock, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_sock,))
        client_handler.start()

if __name__ == "__main__":
    start_server()