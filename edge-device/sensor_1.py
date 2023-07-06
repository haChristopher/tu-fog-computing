import random
import time
import json

class SensorData_1:
    def __init__(self):
        # Define the ranges for random values
        self.temperature_range = (20.0, 26.0)
        self.pressure_range = (1000.0, 1034.0)
        self.humidity_range = (50, 54)
        self.wind_speed_range = (17.0, 38.0)
        self.weather_naming_options = ['Partly cloudy', 'Sunny', 'Rainy', 'Light rain', 'Cloudy']
        self.cities = ['Berlin', 'Hamburg', 'Munich']

    def generate_sensor_data(self):
        current_time = int(time.time())
        time_measurement = current_time 
        temperature = round(random.uniform(*self.temperature_range), 1)
        pressure = round(random.uniform(*self.pressure_range), 1)
        humidity = random.randint(*self.humidity_range)
        wind_speed = round(random.uniform(*self.wind_speed_range), 1)
        weather_naming = random.choice(self.weather_naming_options)
        timestamp_request = time_measurement + random.randint(1, 10)
        # city = random.choice(self.cities)

        sensor_entry = {
            'city': self.cities[0],
            'country': 'Germany',
            'time_of_measurement': time_measurement,
            'temperature': temperature,
            'pressure': pressure,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'weather_naming': weather_naming,
            'timestamp_request': timestamp_request
        }
        return sensor_entry


# Example usage:
if __name__ == '__main__':
    sensor_generator = SensorData_1()
    sensor_data = sensor_generator.generate_sensor_data()
    print(json.dumps(sensor_data, indent=4))
