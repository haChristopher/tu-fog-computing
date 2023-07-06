"""
This needs to be adapted for docker -> add as env variable
PUB/SUB seems to be correct pattern https://zguide.zeromq.org/docs/chapter5/

All Patter: http://api.zeromq.org/2-1%3azmq-socket#toc13

TODO When server is is off client just stops and block it should trow and error
TODO Disable conenction handling
TODO add queue with sender
"""
import os
import sys
import json
import time
import random
import threading
import logging as log

import zmq
import zmq.asyncio

from sensor_1 import SensorData_1
from sensor_2 import SensorData_2
from sensor_3 import SensorData_3
import sqlite_helper as db_helper
from exceptions import NoAckException

# Setup logging
log.basicConfig(stream=sys.stdout, level=log.DEBUG)

# Read environment variables
URL_CLIENT = os.getenv("SERVER_ADDRESS", default="tcp://127.0.0.1:5555")
SELECTED_CITY = os.getenv("CITY", default="Berlin")
DB_NAME = os.getenv("DB_NAME", default="messages.db")

def setup_db(name):
    # Setting up DB if not already exists
    conn = db_helper.create_connection(name)
    db_helper.setup_table(conn)
    conn.close()

def get_socket(address: str):
    context = zmq.Context() # With asyn to much in parallel
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.SNDTIMEO, 0)
    socket.setsockopt(zmq.SNDHWM, 0)
    socket.setsockopt(zmq.SNDBUF, 10) # Zero means underlying default from OS is used
    log.info(f"Connecting to server at {address}")
    socket.connect(address)
    return socket

def db_cleaner():
    conn = db_helper.create_connection(DB_NAME)
    while True:
        db_helper.delete_all_send_message(conn)
        time.sleep(60)


def db_sender():
    socket = get_socket(URL_CLIENT)
    conn = db_helper.create_connection(DB_NAME)
    
    log.info("Connecting to db to check for unsent messages")
    while True:
        id, message = db_helper.get_next_unsend_message(conn)
        if id is not None:
            try:
                log.info(f"Sending unsent message with id {id}")
                socket.send_pyobj(message)
                ack = socket.recv()
                if ack != b'ACK':
                    raise NoAckException("No ACK received")
                db_helper.mark_message_as_send(conn, id)
            except zmq.error.ZMQError as e:
                log.warning("Message could not be send, storing in DB")
                db_helper.increase_send_attempt(conn, id)
            except NoAckException as e:
                log.warning("No ACK received, storing in D")
                db_helper.increase_send_attempt(conn, id)
        
        # time.sleep(2)

def sender():
    socket = get_socket(URL_CLIENT)
    conn = db_helper.create_connection(DB_NAME)

    count = 0
    while True:
        sensor_data = random.choice(sensor_cities).generate_sensor_data()
        try:
            log.info(f"Sending sensor_data - {sensor_data}")
            socket.send_pyobj(sensor_data)
            ack = socket.recv()
            if ack != b'ACK':
                raise NoAckException("No ACK received")
            count += 1
        except zmq.error.ZMQError as e:
            log.warning("Message could not be send, storing in DB")
            data_json = json.dumps(sensor_data)
            db_helper.write_unsend_message(conn, data_json)
        except NoAckException as e:
            log.warning("No ACK received, storing in D")
            db_helper.increase_send_attempt(conn, id)
    
        time.sleep(2)

if __name__ == "__main__":
    log.info("Connecting server...")

    #Setup SensorData, this can be one python file with param
    sensor_generator_1 = SensorData_1()
    sensor_generator_2 = SensorData_2()
    sensor_generator_3 = SensorData_3()
    sensor_cities = [sensor_generator_1, sensor_generator_2, sensor_generator_3]

    # Setup DB
    setup_db(DB_NAME)

    sender_thread = threading.Thread(target=sender, args=())
    db_sender_thread = threading.Thread(target=db_sender, args=())
    db_cleaner_thread = threading.Thread(target=db_cleaner, args=())
    sender_thread.start()
    db_sender_thread.start()
    db_cleaner_thread.start()

    sender_thread.join()
    db_sender_thread.join()

    log.info("Server is closing...")
