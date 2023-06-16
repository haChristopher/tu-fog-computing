import requests, json, time, csv, time, os 


# only TU Berlin as location
lat = 52.5119
lon = 13.3262


#Load config data
config_file = 'config.json'

# Read the data from the config file
with open(config_file) as file:
    config_data = json.load(file)

# Access the data from the config file
URL_base = config_data['URL_base']
api_key = config_data['api_key']
csv_file = config_data['csv_file']
time_delay = config_data['time_delay']


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
                "sunrise_unix":result["current"]["sunrise"],
                "sunset_unix":result["current"]["sunset"],
                "temp":result["current"]["temp"],
                "pressure":result["current"]["pressure"],
                "humidity":result["current"]["humidity"],
                "wind_speed":result["current"]["wind_speed"],
                "weather_naming":result["current"]["weather"][0]["description"],
                "timestamp":int(time.time())
            }
            append_json_to_csv(resp_obj)
        else:
            raise Exception ("Error parsing data - {}".format(s.status_code))
    except Exception as e:
        print("[weather-parser] - Error [{0}]".format(e))


def append_json_to_csv(json_data):
    if not os.path.isfile(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=json_data.keys())
            writer.writeheader()

    with open(csv_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=json_data.keys())
        writer.writerow(json_data)
    print("[weather-parser] - Successfully parsed weather [{0},{1}] and inserted into {2}".format(lat, lon, csv_file))



if __name__ == "__main__":
    while True:
        get_current_weather()
        time.sleep(time_delay)