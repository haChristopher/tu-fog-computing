import random
import time
import json
import requests


# Read the data from the config file
with open("config.json") as file:
    config_data = json.load(file)

api_key = config_data['api_key']
simulate_data = config_data['simulate_data']
generate_data = simulate_data.lower() == 'true'
generate_data = False

class SensorData_3:
    def __init__(self):
        # Define the ranges for random values
        self.temperature_range = (20.0, 25.0)
        self.pressure_range = (1034.0, 1061.0)
        self.humidity_range = (51, 64)
        self.wind_speed_range = (30.0, 39.0)
        self.weather_naming_options = ['Partly cloudy', 'Sunny', 'Rainy', 'Light rain', 'Cloudy']
        self.cities = ['Berlin', 'Hamburg', 'Munich']


    def generate_sensor_data(self):
        if(generate_data == True):
            print(f"[weather-parser] - Simulating environmental data for [{self.cities[2]}]")
            current_time = int(time.time())
            time_measurement = current_time 
            temperature = round(random.uniform(*self.temperature_range), 1)
            pressure = round(random.uniform(*self.pressure_range), 1)
            humidity = random.randint(*self.humidity_range)
            wind_speed = round(random.uniform(*self.wind_speed_range), 1)
            weather_naming = random.choice(self.weather_naming_options)
            timestamp_request = time_measurement + random.randint(1, 10)


            sensor_entry = {
                'city': self.cities[2],
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
        else:
            try:
                print(f"[weather-parser] - Parsing environmental data from API for [{self.cities[2]}]")
                city = self.cities[2]
                url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
                x = requests.Session()
                s = x.get(url)
                if(s.status_code == 200):
                    result = json.loads(s.text)
                    resp_obj = {
                        "city":city,
                        "country":result["location"]["country"],
                        #"time_of_measurement":result["location"]["localtime_epoch"],
                        "time_of_measurement":int(time.time()),
                        "temperature":result["current"]["temp_c"],
                        "pressure":result["current"]["pressure_mb"],
                        "humidity":result["current"]["humidity"],
                        "wind_speed":result["current"]["wind_kph"],
                        "weather_naming":result["current"]["condition"]["text"],
                        "timestamp_request":int(time.time())
                    }
                    return resp_obj
                else:
                    raise Exception ("Error parsing data - {}".format(s.status_code))
            except Exception as e:
                print("[weather-parser] - Error [{0}]".format(e))
                return None


# Example usage:
if __name__ == '__main__':
    sensor_generator = SensorData_3()
    sensor_data = sensor_generator.generate_sensor_data()
    print(json.dumps(sensor_data, indent=4))
