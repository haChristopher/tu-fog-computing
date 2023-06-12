import time
import zmq
from util import average_sensor_data


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

    # receive sensor data
    data = socket.recv_pyobj()
    print("Received sensor data from client: % s" % data)
    print("Processing ... Processing")
    print()

    # decode a byte into a str --> decode()
    # print("Received request from client: %s" % message.decode())

    #  Do some 'work'
    time.sleep(2)
    average_data = average_sensor_data(data)
    # print(average_data)

    #  Send reply back to client
    # socket.send(b"World", track=True)
    socket.send_pyobj(average_data)