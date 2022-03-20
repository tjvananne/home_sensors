import json
import re
import time
import requests
from LAN_forwarder import make_time_fields

# ==== adhoc, testing out dict-to-json string, then writing that to postgres =====

x = {'coord': {'lon': -6, 'lat': 32},
 'weather': [{'id': 800,
   'main': 'Clear',
   'description': 'clear sky',
   'icon': '01d'}],
 'base': 'stations',
 'main': {'temp': 36.88,
  'feels_like': 34.3,
  'temp_min': 31.15,
  'temp_max': 44.74,
  'pressure': 1021,
  'humidity': 51},
 'visibility': 10000,
 'wind': {'speed': 3.44, 'deg': 210},
 'clouds': {'all': 0},
 'dt': 1647354130,
 'sys': {'type': 2,
  'id': 2005772,
  'country': 'US',
  'sunrise': 1647349951,
  'sunset': 1647392848},
 'timezone': -21600,
 'id': 5574991,
 'name': 'some_city',
 'cod': 200}


json.dumps(x)


# ==== old for reference (testing out the API) =====

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

