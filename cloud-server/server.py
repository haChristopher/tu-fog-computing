import sys
import os
import json
import time
import threading
import requests
import logging as log

import zmq

# Setup logging
log.basicConfig(stream=sys.stdout, level=log.DEBUG)

URL_CLIENT = os.getenv("SERVER_ADDRESS", default="tcp://*:5555")
BACKEND_ENDPOIMT = os.getenv("SERVER_ENDPOINT", default="http://127.0.0.1:5000")

def post_to_flask(json_data):
    try:
        full_endpoint = BACKEND_ENDPOIMT + "/api/v2/submit"
        requests.post(full_endpoint, json=json_data)
        log.info("Sent sensor data to flask: % s" % json_data)
    except Exception as e:
        # TODO: Handle errors
        log.error(e)

def msg_receiver():
    log.debug("Server is starting ...")

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    # socket.setsockopt(zmq.HWM, 0)
    socket.bind(URL_CLIENT)

    log.debug("Waiting for messages ...")
    while True:
        # receive sensor data
        data = socket.recv_pyobj()
        log.info("Received sensor data from client: % s" % data)
        socket.send_string("ACK")
        
        # send sensor data to flask
        post_to_flask(json.dumps(data))

    

if __name__ == "__main__":
    # Setup a sender an receiver thread
    # Just reuse the client as same code.
    receive_thread = threading.Thread(target=msg_receiver, args=())
    
    # Start and join threads
    receive_thread.start()
    receive_thread.join()