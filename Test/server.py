import time
import zmq

url_client = "tcp://*:5555"

# A context creates sockets
context = zmq.Context()
# or zmq.PUB
# socket of type RESPONSE
socket = context.socket(zmq.REP)
socket.bind(url_client)

# server waits now for messages ...

# EXAMPLE_1
while True:
    #  Wait for next request from client
    message = socket.recv()
    # decode a byte into a str --> decode()
    print("Received request from client: %s" % message.decode())

    #  Do some 'work'
    time.sleep(2)

    #  Send reply back to client
    socket.send(b"World", track=True)
