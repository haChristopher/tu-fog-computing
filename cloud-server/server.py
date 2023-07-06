import sys
import os
import time
import logging as log

import zmq

# Setup logging
log.basicConfig(stream=sys.stdout, level=log.DEBUG)

URL_CLIENT = os.getenv("SERVER_ADDRESS", default="tcp://*:5555")

def post_to_flask():
    pass

def msg_receiver():
    log.debug("Server is starting ...")

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.setsockopt(zmq.HWM, 0)
    socket.setsockopt(zmq.SNDTIMEO, 0)
    socket.bind(URL_CLIENT)

    log.debug("Waiting for messages ...")
    while True:
        # receive sensor data
        data = socket.recv_pyobj()
        log.info("Received sensor data from client: % s" % data)
        socket.send_string("ACK")

    



if __name__ == "__main__":
    # Setup a sender an receiver thread
    # Just reuse the client as same code.
    run()