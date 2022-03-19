from flask import Flask, request
import logging
import json
from tasks import load_sensor
from utils import all_valid, make_time_fields


# ==== Config ====


MEASUREMENTS = ['temperature', 'humidity', 'pressure', 'lastCheckin']

logging.basicConfig(
    filename="LAN_forwarder.log", 
    format='[%(asctime)s.%(msecs)03d][%(levelname)s] %(message)s', 
    level=logging.DEBUG, 
    datefmt='%Y-%m-%d %H:%M:%S')


# ==== Flask App ====


app = Flask(__name__)

@app.route("/hello", methods=['GET'])
def hello():
    """
    hello world route for interactively ensuring docker compose is up.
    """
    print("I ran the 'hello' route!")
    return '<p>Hello, World!</p>'


@app.route("/sensor", methods=['POST'])
def receive_sensor_data():

    # extract JSON into dict    
    content_raw = request.json
    content = content_raw.get('content')
    print("\n\n------------")
    print("printing content!")
    print(content)

    # stop if JSON is not formatted according to our assumptions
    if not content:
        raw_json_string = json.dumps(content)
        logging.warning(f"Improper JSON format: {raw_json_string}")
        return '200'
    
    # choosing consistency over Python style guidelines
    displayName = content.get("displayName")
    name = content.get("name")
    value = content.get("value")
    unit = content.get("unit")
    deviceId = content.get("deviceId")

    # quick patch for "lastCheckin" units (so we actually record those...)
    if name == "lastCheckin":
        unit = "timestamp" 

    if not name:
        raw_json_string = json.dumps(content)
        logging.warning(f"No 'name' field in JSON payload: {raw_json_string}")

    # filter to only the measurements we're interested in
    if not name in MEASUREMENTS:
        raw_json_string = json.dumps(content)
        logging.info(f"Not a measurement we're interested in: {raw_json_string}")
        return '200'
    
    # stop if JSON is not formatted according to our assumptions
    if not all_valid(displayName, name, value, unit, deviceId):
        raw_json_string = json.dumps(content)
        logging.warning(f"Improper JSON format: {raw_json_string}")
        return '200'

    # preprocess sensor data
    del content['descriptionText']
    del content['type']
    del content['data']
    utc_ts, mtn_ts, mtn_date, mtn_time = make_time_fields()
    content['utc_LAN_received'] = utc_ts
    content['utc_cloud_insertion'] = utc_ts
    content['mtn_date'] = mtn_date
    content['mtn_time'] = mtn_time

    # load sensor data
    print("calling load_sensor.delay(content)...")
    load_sensor.delay(content)
    print("done.")
    return '200'


if __name__ == "__main__":

    # Note, this is for testing only...
    # In prod, use gunicorn like so:
    # gunicorn --bind 0.0.0.0:5000 LAN_forwarder:app
    app.run(host='0.0.0.0', port=5000, debug=True)
