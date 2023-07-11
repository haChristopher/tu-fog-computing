"""
This needs to be adapted for docker -> add as env variable
PUB/SUB seems to be correct pattern https://zguide.zeromq.org/docs/chapter5/

All Patterns: http://api.zeromq.org/2-1%3azmq-socket#toc13
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
from logging_formatter import WeatherStationFormatter


# Read environment variables
URL_CLIENT = os.getenv("SERVER_ADDRESS", default="tcp://127.0.0.1:5555")
SELECTED_CITY = os.getenv("CITY", default="Berlin")
DB_NAME = os.getenv("DB_NAME", default="messages.db")
REQUEST_TIMEOUT = os.getenv("REQUEST_TIMEOUT", default=1000)
REQUEST_RETRIES = os.getenv("REQUEST_RETRIES", default=3)
CLIENT_ID = os.getenv("CLIENTID", default=random.randint(0, 1000000))

# Setup logging
w_log = log.getLogger("My_app")
w_log.setLevel(log.DEBUG)
ch = log.StreamHandler()
ch.setLevel(log.DEBUG)
ch.setFormatter(WeatherStationFormatter())
w_log.propagate = False
w_log.addHandler(ch)


"""Setup DB if not already exists"""
def setup_db(name):
    conn = db_helper.create_connection(name)    
    db_helper.setup_table(conn)
    conn.close()

"""Get socket with default settings"""
def get_socket(address: str):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.SNDTIMEO, REQUEST_TIMEOUT)
    socket.setsockopt(zmq.RCVTIMEO, REQUEST_TIMEOUT)
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


def handle_response(response):
    try:
        if len(response["alerts"]) > 0:
            for alert in response["alerts"]:
                if alert["level"] == "HIGH":
                    w_log.critical(f"Alerts: {alert['message']}")
                else:
                    w_log.error(f"Alerts: {alert['message']}")
        if len(response["maintenance_schedule"]) > 0:
            for maintenance in response["maintenance_schedule"]:
                w_log.info(f"Planned maintenance: {maintenance['message']} at {maintenance['time']}")
        if len(response["weather_forecast"]) > 0:
            for forecast in response["weather_forecast"]:
                w_log.info(f"Weather forecast: {forecast['message']} at {forecast['time']}")

    except Exception as e:
        log.error("Error parsing response")

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
        response = socket.recv_pyobj()
        if not response["ack"]:
            raise NoAckException("No ACK received")
        handle_response(response["data"])
        return True
    except zmq.error.ZMQError as e:
        log.warning("Message could not be send, storing in DB")
        return False
    except NoAckException as e:
        log.warning("No ACK received, storing in DB")
        return False
    except Exception as e:
        log.error(e)
        return False


"""Check DB for unsend messages and send them"""
def db_sender():
    log.info("Connecting to db to check for unsent messages")
    db_conn = db_helper.create_connection(DB_NAME)
    while True:
        retries = 0

        socket = get_socket(URL_CLIENT)

        # After a certain amount of retries, the connection will be recreated
        while retries < REQUEST_RETRIES:
            id, message = db_helper.get_next_unsend_message(db_conn)
            log.info(f"Resending message with id {id}")
            if id is not None:
                message = json.loads(message)
                success = handle_send_message(socket, message)
                
                if success:
                    db_helper.mark_message_as_send(db_conn, id)
                    retries = 0
                    w_log.debug("Message resent successfully")
                else:
                    db_helper.increase_send_attempt(db_conn, id)
                    retries += 1
            
            time.sleep(2)

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
                w_log.debug("Message sent successfully")
            else:
                data_json = json.dumps(message)
                db_helper.write_unsend_message(db_conn, data_json)
                retries += 1
            time.sleep(2)

        socket.close()


def data_generator_runner(sensor_generator, queue):
    while True:
        sensor_data = sensor_generator.generate_sensor_data()
        queue.put(sensor_data)
        time.sleep(0.5)


if __name__ == "__main__":
    log.info("Connecting server...")

    #Setup SensorData, this can be one python file with param
    sensor_generator_1 = SensorData_1()
    sensor_generator_2 = SensorData_2()
    sensor_generator_3 = SensorData_3()
    sensor_cities = {
        "Berlin": sensor_generator_1,
        "Hamburg": sensor_generator_2,
        "Munich": sensor_generator_3
    }

    # Select sensor
    selected_sensor = sensor_cities[SELECTED_CITY]

    # Setup DB
    setup_db(DB_NAME)

    # Sensor data queue
    queue = queue.Queue()

    # Setup Threads
    data_generator_thread = threading.Thread(target=data_generator_runner, args=(selected_sensor, queue))
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
