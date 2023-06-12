import requests
import json 
import time 
import csv


CSV_name = "weatherdata.csv"
URL_base = "http://api.weatherapi.com/v1"
api_key = "e6f2e34add2d1ba268283797394bc32f"
csv_file = "weather.csv"
time_delay = 3600 # every hour
lat = 52.5119
lon = 13.3262

def get_current_weather():
    try:
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&lang=de"
        x = requests.Session()
        s = x.get(url)
        if(s.status_code == 200):
            result = json.loads(s.text)
            resp_obj = {
                "lat":lat,
                "lon":lon,
                "timezone":result["timezone"],
                "timestamp":int(time.time()),
                "current_data":result["current"]
            }
            print("[weather-parser] - Successfully parsed weather [{0},{1}]".format(lat, lon))
            append_json_to_csv(resp_obj)
        else:
            raise Exception ("Error parsing data - {}".format(s.status_code))
        
    except Exception as e:
        print("[weather-parser] - Error [{0}]".format(e))

def append_json_to_csv(json_data):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([json.dumps(json_data)])
        print("[weather-parser] - Successfully inserted into {}".format(csv_file))

if __name__ == "__main__":
    while True:
        get_current_weather()
        #parse every hour
        time.sleep(time_delay)