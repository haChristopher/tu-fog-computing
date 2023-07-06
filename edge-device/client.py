import os
import sys
import time
import random
import logging as log
from sensor import SensorDataGenerator
import zmq
import zmq.asyncio

# Setup logging
log.basicConfig(stream=sys.stdout, level=log.DEBUG)

# This needs to be adapted for docker -> add as env variable

url_client = os.getenv("SERVER_ADDRESS", default="tcp://127.0.0.1:5555")

# A context creates sockets
context = zmq.asyncio.Context()
print("Connecting to hello world server...")

socket = context.socket(zmq.PUSH)
socket.setsockopt(zmq.SNDHWM, 0)
socket.setsockopt(zmq.SNDBUF, 0)
socket.connect(url_client)
sensor_generator = SensorDataGenerator()

def run():
    while True:
        sensor_data = sensor_generator.generate_sensor_data()
        log.info(f"Sending sensor_data - {sensor_data}")
        socket.send_pyobj(sensor_data)

        time.sleep(4)


if __name__ == "__main__":
    log.info("Connecting server...")
    run()