import time
import zmq

url_client = "tcp://*:5555"

# A context creates sockets
context = zmq.Context()
# or zmq.PUB
socket = context.socket(zmq.REP)
socket.bind(url_client)

# EXAMPLE_1
# logic of the messaging
# message = [100, 200, 300]
# curMsg = 0

# while True:
#     time.sleep(1)
#     socket.send_pyobj({curMsg: message[curMsg]})
#     if (curMsg == 2):
#         curMsg = 0
#     else:
#         curMsg += 1

# EXAMPLE_2
while True:
    #  Wait for next request from client
    message = socket.recv()
    # decode a byte into a str --> decode()
    print("Received request from client: %s" % message.decode())

    #  Do some 'work'
    time.sleep(2)

    #  Send reply back to client
    socket.send(b"World", track=True)
