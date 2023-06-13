import zmq
import zmq.asyncio

url_client = "tcp://localhost:5555"

context = zmq.asyncio.Context()
# Socket to talk to server
print("Connecting to hello world server...")
# socket of type REQUEST

socket = context.socket(zmq.PUSH)
socket.setsockopt(zmq.HWM, 0)
socket.connect(url_client)

# EXAMPLE_1

data1 = [765, 2345, 6, 26]
data2 = [463646, 3, 31, 67354]
data3 = [656, 346, 34, 24]
data4 = [1, 63463, 82, 745]
data5 = [34, 6346, 2, 266]
data6 = [2343432, 34, 8232, 5246543]
data7 = [34, 734, 823, 235]
data8 = [346, 34, 23, 523]

data_set = [data1, data2, data3, data4, data5, data6, data7, data8]

#  Do 10 requests, waiting each time for a response
for request in range(len(data_set)):
    print("Sending sensor data %s" % data_set[request])
    socket.send_pyobj(data_set[request])
    # socket.send(b"Hello")

    # Get the reply
    # processed_data = socket.recv_pyobj()
    # decode a byte into a str --> decode()
    # print("Received reply %s [%s]" % (request, message.decode()))
    
    # print("Received average processed data: %s" % processed_data)


if __name__ == "__main__":
    print("Connecting to hello world server...")