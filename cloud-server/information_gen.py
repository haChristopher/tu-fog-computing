"""
    Should we fetch that from an api ?
"""
import random
import datetime
from datetime import timedelta

CITIES = ['Berlin', 'Hamburg', 'Munich']
MAINTENANCE_TYPES = ['maintenance', 'repair', 'inspection']
ALERT_LEVELS = ['HIGH', 'MEDIUM', 'LOW']
ALERT_MESSAGES = ['Storm', "Orkan", "Flood", "Sandstorm"]
WEATHER_FORCASTS = ['Sunny', 'Rainy', 'Cloudy', 'Snowy', 'Windy', 'Stormy', 'Foggy', 'Hail', 'Thunderstorm', 'Sleet', 'Shower', 'Drizzle', 'Haze', 'Smoky', 'Freezing', 'Overcast', 'Partly cloudy', 'Clear', 'Mostly cloudy', 'Scattered clouds', 'Broken clouds', 'Few clouds', 'Unknown']

def get_random_date_in_future():
    start_date = datetime.datetime.now()
    end_date = start_date + timedelta(days=10)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d %H:%M:%S")

def get_generated_information(server_id: int):
    # get random city
    city = random.choice(CITIES)
    alerts = []
    maintenance_schedule = []
    weather_forecast = []

    # only in 10% of the time genereate alerts
    if random.random() < 0.1:
        alerts.append({
            "id": 1, 
            "message": random.choice(ALERT_MESSAGES),
            "time": get_random_date_in_future(),
            "level": random.choice(ALERT_LEVELS)
        })

    # only in 80% of the time genereate maintenance
    if random.random() < 0.8:
        maintenance_schedule.append({
            "id": 1, 
            "message": random.choice(MAINTENANCE_TYPES),
            "time": get_random_date_in_future(),
        })

    # only in 80% of the time genereate weather forecast
    if random.random() < 0.8:
        random_time_in_future = random.randint(1, 1000)
        weather_forecast.append({
            "id": 1, 
            "message": random.choice(WEATHER_FORCASTS),
            "time": get_random_date_in_future(),
        })

    return {
        "alerts": alerts,
        "maintenance_schedule": maintenance_schedule,
        "weather_forecast": weather_forecast,
    }, city
           

def merge_list_of_information(infos: list):
    alerts = []
    maintenance_schedule = []
    weather_forecast = []

    for info in infos:
        alerts += info["alerts"]
        maintenance_schedule += info["maintenance_schedule"]
        weather_forecast += info["weather_forecast"]

    return {
        "alerts": alerts,
        "maintenance_schedule": maintenance_schedule,
        "weather_forecast": weather_forecast,
    }