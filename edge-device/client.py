"""
This needs to be adapted for docker -> add as env variable
PUB/SUB seems to be correct pattern https://zguide.zeromq.org/docs/chapter5/

All Patter: http://api.zeromq.org/2-1%3azmq-socket#toc13

TODO When server is is off client just stops and block it should trow and error
TODO Disable conenction handling
"""
import os
import sys
import json
import queue
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


# Read environment variables
URL_CLIENT = os.getenv("SERVER_ADDRESS", default="tcp://127.0.0.1:5555")
SELECTED_CITY = os.getenv("CITY", default="Berlin")
DB_NAME = os.getenv("DB_NAME", default="messages.db")
REQUEST_TIMEOUT = os.getenv("REQUEST_TIMEOUT", default=1000)
REQUEST_RETRIES = os.getenv("REQUEST_RETRIES", default=6)
CLIENT_ID = os.getenv("CLIENTID", default=random.randint(0, 1000000))

# Setup logging
log.basicConfig(stream=sys.stdout, level=log.DEBUG)


"""Setup DB if not already exists"""
def setup_db(name):
    conn = db_helper.create_connection(name)    
    db_helper.setup_table(conn)
    conn.close()

"""Get socket with default settings"""
def get_socket(address: str):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.SNDTIMEO, 1000)
    socket.setsockopt(zmq.RCVTIMEO, 1000)
    socket.setsockopt(zmq.SNDHWM, 0)
    socket.setsockopt(zmq.LINGER, 0)
    socket.setsockopt(zmq.SNDBUF, 1) # Zero means underlying default from OS is used
    log.info(f"Connecting to server at {address}")
    socket.connect(address)
    return socket


"""Periodically clean the DB of sent messages"""
def db_cleaner():
    conn = db_helper.create_connection(DB_NAME)
    while True:
        db_helper.delete_all_send_message(conn)
        time.sleep(60)

"""
    Send message to server and handle errors:
        socket: zmq socket
        db_conn: sqlite connection
        message: message to send
        is_retry: is this a retry message (if yes DB will be updated)
"""""
def handle_send_message(socket, message) -> bool:
    try:
        # log.info(f"Sending sensor_data - {message}")
        socket.send_pyobj(message)
        ack = socket.recv()
        if ack != b'ACK':
            raise NoAckException("No ACK received")
        return True
    except zmq.error.ZMQError as e:
        log.warning("Message could not be send, storing in DB")
        return False
    except NoAckException as e:
        log.warning("No ACK received, storing in D")
        return False


"""Check DB for unsend messages and send them"""
def db_sender():
    log.info("Connecting to db to check for unsent messages")
    db_conn = db_helper.create_connection(DB_NAME)
    while True:
        retries = 0

        socket = get_socket(URL_CLIENT)
        while retries < REQUEST_RETRIES:
            id, message = db_helper.get_next_unsend_message(db_conn)
            if id is not None:
                success = handle_send_message(socket, message)
                
                if success:
                    db_helper.mark_message_as_send(db_conn, id)
                    retries = 0
                else:
                    db_helper.increase_send_attempt(db_conn, id)
                    retries += 1
            
            time.sleep(0.1)

        socket.close()

"""Send newest incoming sensor data to server"""
def sender(queue):
    db_conn = db_helper.create_connection(DB_NAME)
    
    while True:
        retries = 0

        socket = get_socket(URL_CLIENT)
        while retries < REQUEST_RETRIES:
            message = queue.get()
            success = handle_send_message(socket, message)
            if success:
                retries = 0
            else:
                data_json = json.dumps(message)
                db_helper.write_unsend_message(db_conn, data_json)
                retries += 1
            time.sleep(0.1)

        socket.close()


def data_generator_runner(sensor_generator, queue):
    for i in range(50):
        sensor_data = sensor_generator.generate_sensor_data()
        queue.put(sensor_data)
        time.sleep(0.5)


if __name__ == "__main__":
    log.info("Connecting server...")

    #Setup SensorData, this can be one python file with param
    sensor_generator_1 = SensorData_1()
    sensor_generator_2 = SensorData_2()
    sensor_generator_3 = SensorData_3()
    sensor_cities = [sensor_generator_1, sensor_generator_2, sensor_generator_3]

    # Setup DB
    setup_db(DB_NAME)

    # Sensor data queue
    queue = queue.Queue()

    # Setup Threads
    data_generator_thread = threading.Thread(target=data_generator_runner, args=(sensor_generator_1, queue))
    sender_thread = threading.Thread(target=sender, args=(queue, ))
    db_sender_thread = threading.Thread(target=db_sender, args=())
    db_cleaner_thread = threading.Thread(target=db_cleaner, args=())
    
    sender_thread.start()
    data_generator_thread.start()
    db_sender_thread.start()
    db_cleaner_thread.start()

    sender_thread.join()
    data_generator_thread.join()
    db_sender_thread.join()
    db_cleaner_thread.join()

    log.info("Server is closing...")
