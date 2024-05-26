import socket
import threading
import time

# Configuration settings for the UDP server
localIP = "0.0.0.0"  # Listens on all network interfaces
localPort = 5051  # Port number to listen on
bufferSize = 1024  # Buffer size for receiving data
broadcastIP = "192.168.88.255"  # Broadcast IP address for sending messages

# Create a UDP socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Enable broadcasting mode on the socket
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to the specified IP and port
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening on port 5051")

# List to store received messages
messages = []

# Function to handle receiving messages
def receiveMessages():
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        sender = f"{address[0]}"
        received_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # Decode the received message
        message = message.decode("utf-8")

        # Append message to the messages list with sender and timestamp
        messages.append((sender, received_time, message))

        # Print received message details
        print(f"Received a message from {sender} at {received_time}")
        for idx, msg in enumerate(messages):
            print(f"{idx + 1}- Received a message from {msg[0]} at {msg[1]}")

# Function to handle sending messages and processing commands
def sendMessages():
    while True:
        input_str = input("Enter your first name, last name, and message or command: ")
        if 'D' in input_str:
            # Display the detail of a specific message if 'D' is included in the input
            line_number = int(input_str.replace('D', '')) - 1
            if 0 <= line_number < len(messages):
                sender, time_received, message = messages[line_number]
                print(f"Detail of message {line_number + 1}: From {sender} at {time_received}: '{message}'")
            else:
                print("Invalid message number.")
        else:
            # Send a message if no command is included
            try:
                firstName, lastName, msg = input_str.split(maxsplit=2)
                fullMessage = f"{firstName} {lastName}: {msg}"
                UDPServerSocket.sendto(fullMessage.encode(), (broadcastIP, localPort))
            except ValueError:
                print("Error: Please enter both your first name, last name and a message.")

# Create threads for receiving and sending messages
receiveThread = threading.Thread(target=receiveMessages)
sendThread = threading.Thread(target=sendMessages)

# Start both threads
receiveThread.start()
sendThread.start()

# Prevent the main thread from exiting by joining the child threads
receiveThread.join()
sendThread.join()
