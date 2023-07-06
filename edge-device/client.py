import os
import sys
import time
import random
import logging as log
from sensor_1 import SensorData_1
from sensor_2 import SensorData_2
from sensor_3 import SensorData_3
import zmq
import zmq.asyncio

# Setup logging
log.basicConfig(stream=sys.stdout, level=log.DEBUG)

#Setup SensorData
sensor_generator_1 = SensorData_1()
sensor_generator_2 = SensorData_2()
sensor_generator_3 = SensorData_3()
sensor_cities = [sensor_generator_1, sensor_generator_2, sensor_generator_3]

# This needs to be adapted for docker -> add as env variable

url_client = os.getenv("SERVER_ADDRESS", default="tcp://127.0.0.1:5555")

# A context creates sockets
context = zmq.asyncio.Context()
print("Connecting to hello world server...")

socket = context.socket(zmq.PUSH)
socket.setsockopt(zmq.SNDHWM, 0)
socket.setsockopt(zmq.SNDBUF, 0)
socket.connect(url_client)


def run():
    while True:
        sensor_data = random.choice(sensor_cities).generate_sensor_data()
        log.info(f"Sending sensor_data - {sensor_data}")
        socket.send_pyobj(sensor_data)
        time.sleep(4)


if __name__ == "__main__":
    log.info("Connecting server...")
    run()