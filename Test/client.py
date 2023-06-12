import zmq

url_client = "tcp://localhost:5555"

context = zmq.Context()
# Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect(url_client)

# EXAMPLE_1
# socket.setsockopt_string(zmq.SUBSCRIBE,  "")

# listeners = [1, 2]

# while True:
#     message = socket.recv_pyobj()
#     msgIndex = message.keys()[0]
#     if (msgIndex in listeners):
#         print(message.get(listeners[msgIndex]))


# EXAMPLE_2

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s" % request)
    socket.send(b"Hello")

    # Get the reply
    message = socket.recv()
    # decode a byte into a str --> decode()
    print("Received reply %s [%s]" % (request, message.decode()))
