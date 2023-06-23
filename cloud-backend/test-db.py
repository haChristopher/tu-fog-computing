import requests
import json

def send_post_request(url, data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print(f"POST request successful. Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during the POST request: {str(e)}")


# Example usage:
url = 'http://127.0.0.1:5000/api/v1'
json_data = {
    "lat": 52.5119,
    "lon": 13.3262,
    "timezone": "Europe/Berlin",
    "sunrise_unix": 1686883390,
    "sunset_unix": 1686943891,
    "temp": 288.64,
    "pressure": 1008,
    "humidity": 90,
    "wind_speed": 3.09,
    "weather_naming": "Leichter Regen",
    "timestamp": 1686899419
}

send_post_request(url, json_data)
