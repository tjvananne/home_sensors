import json
import re
import time
import requests
from LAN_forwarder import make_time_fields

with open("secrets.json", "r") as f:
    secrets = json.load(f)

apikey = secrets.get("openweathermap")
lat    = secrets.get("lat")
lon    = secrets.get("lon")

while True:

    resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units=imperial")
    this_timestamp = re.sub('[- :\.]', '_', make_time_fields()[1])
    weather_data = json.loads(resp.text)
    
    with open('data/json_weather_' + this_timestamp + ".json", "w") as f:
        json.dump(weather_data, f)
    
    print(json.dumps(weather_data, indent=2))
    
    time.sleep(10 * 60)

