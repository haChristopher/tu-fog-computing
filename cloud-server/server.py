import sys
import os
import json
import random
import threading
import requests
import logging as log

import zmq


# Read environment variables
URL_CLIENT = os.getenv("SERVER_ADDRESS", default="tcp://*:5555")
BACKEND_ENDPOIMT = os.getenv("SERVER_ENDPOINT", default="http://127.0.0.1:5000")
SERVER_ID = os.getenv("SERVER_ID", default=random.randint(0, 1000000))

# Setup logging
log.basicConfig(stream=sys.stdout, level=log.DEBUG)


"""Calculate information for edge device to send back to edge device"""
def getInformationForEdgeDevice(device_id: int) -> object:
    return {
        "id": SERVER_ID,
        "ack": True,
        "warnings": [],
        "alerts": [
            {
                "id": 1, 
                "message": "STORM !!!! PANIC",
                "time": "2020-12-12 12:12:12",
                "level": "HIGH"
            }
        ],
        "maintenance_schedule": [],
        "weather_forecast": [],
    }


"""Send sensor data to flask endpoint to store in DB"""
def post_to_flask(json_data):
    try:
        full_endpoint = BACKEND_ENDPOIMT + "/api/v2/submit"
        requests.post(full_endpoint, json=json_data)
        # log.info("Sent sensor data to flask: % s" % json_data)
    except Exception as e:
        # TODO: Handle errors
        log.error(e)

"""Receive messages from edge device and send to flask"""
def msg_receiver():
    count = 0
    log.debug("Server is starting ...")

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(URL_CLIENT)

    log.debug("Waiting for messages ...")
    while True:
        # receive sensor data
        data = socket.recv_pyobj()
        # log.info("Received sensor data from client: % s" % data)
        
        response_obj = getInformationForEdgeDevice(3)
        socket.send_string("ACK")
        count += 1
        log.info(f"Received Messages: {count}")
        # socket.send_pyobj(response_obj)
        
        # send sensor data to flask
        # post_to_flask(json.dumps(data))

    

if __name__ == "__main__":
    # Setup a sender an receiver thread
    # Just reuse the client as same code.
    receive_thread = threading.Thread(target=msg_receiver, args=())
    
    # Start and join threads
    receive_thread.start()
    receive_thread.join()