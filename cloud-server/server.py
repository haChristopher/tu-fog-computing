import sys
import time
import logging as log

import zmq

# Setup logging
log.basicConfig(stream=sys.stdout, level=log.DEBUG)

url_client = "tcp://*:5555"

log.debug("Server is starting ...")

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.setsockopt(zmq.RCVBUF, 0)
socket.bind(url_client)

log.debug("Waiting for messages ...")
while True:
    # receive sensor data
    data = socket.recv_pyobj()
    log.info("Received sensor data from client: % s" % data)
    time.sleep(2)