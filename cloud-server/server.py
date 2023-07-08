import os
import sys
import json
import time
import random
import threading
import requests
import logging as log

import zmq

from information_gen import get_generated_information, merge_list_of_information
import sqlite_helper as db_helper

# Read environment variables
URL_CLIENT = os.getenv("SERVER_ADDRESS", default="tcp://*:5555")
BACKEND_ENDPOIMT = os.getenv("SERVER_ENDPOINT", default="http://127.0.0.1:5000")
SERVER_ID = os.getenv("SERVER_ID", default=random.randint(0, 1000000))
DB_NAME = os.getenv("DB_NAME", default="informations.db")

# Setup logging
log.basicConfig(stream=sys.stdout, level=log.DEBUG)


def edge_device_information_generator():
    conn = db_helper.create_connection(DB_NAME) 
    
    while True:
        response_obj, city = get_generated_information(SERVER_ID)
        db_helper.write_information_to_db(conn, json.dumps(response_obj), city)
        log.info(f"Generated Messages ..")
        time.sleep(1)

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

    conn = db_helper.create_connection(DB_NAME) 

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(URL_CLIENT)

    log.debug("Waiting for messages ...")
    while True:
        # receive sensor data
        data = socket.recv_pyobj()
        # log.info("Received sensor data from client: % s" % data)

        log.info(f"Received Messages: {data}")
        city = data["city"]
        
        # Get amd parse messages from DB
        rows = db_helper.get_all_information_for_city(conn, city)
        ids = [row[0] for row in rows]
        messages = [json.loads(row[1]) for row in rows]

        response_data = merge_list_of_information(messages)
        response_obj = {
            "server_id": SERVER_ID,
            "ack": True,
            "data": response_data
        }
        socket.send_pyobj(response_obj)
        db_helper.delete_messages_by_ids(conn, ids)

        count += 1
        log.info(f"Received Messages: {count}")
        # socket.send_pyobj(response_obj)
        
        # send sensor data to flask
        # post_to_flask(json.dumps(data))

    

if __name__ == "__main__":
    # Setup a sender an receiver thread
    # Just reuse the client as same code.

    # Setup DB if not already exists
    conn = db_helper.create_connection(DB_NAME) 
    db_helper.setup_table(conn)
    conn.close()

    information_generator_thread = threading.Thread(target=edge_device_information_generator, args=())
    receive_thread = threading.Thread(target=msg_receiver, args=())
    
    # Start and join threads
    information_generator_thread.start()
    receive_thread.start()
    receive_thread.join()
    information_generator_thread.join()