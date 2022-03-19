import json
import re
from my_celery_app import app
from celery.signals import worker_init
from sqlalchemy import create_engine, text
import requests
from utils import make_time_fields

# this is essentially what I'm attempting..
# https://stackoverflow.com/questions/14526249/celery-worker-database-connection-pooling

# TODO: do the sqlalchemy connections in my @worker_init.connect function need to be global?

@app.task
def get_and_load_weather_data() -> str:
    """
    Requests data from a weather API, stores that into the database.
    """
    
    # TODO: let's just see if we can get this up and running before setting up database schema and all that
    resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units=imperial")

    this_timestamp = re.sub('[- :\.]', '_', make_time_fields()[1])
    weather_data = json.loads(resp.text)  
    print("=" * 30, "weather data test", "=" * 30)  
    print(this_timestamp)    
    print(json.dumps(weather_data, indent=2))


@app.task
def load_sensor(data_dict: dict) -> str:
    """
    Task responsible for parsing JSON data into SQL query strings, then loading
    that data into a local and cloud database.

    Call this in Flask app like:
    >>> load_sensor.delay(content)
    where "content" is the dict that represents our JSON data.

    Returns a string '200' HTTP code if successful.
    """

    print("Loading sensor data")

    # eng_local is a global... it will exist on all workers
    with eng_local.begin() as conn:
        conn.execute(
            text("""INSERT INTO boulder.sensor (
                        displayName, name, value, unit, deviceId, 
                        utc_LAN_received, utc_cloud_insertion, 
                        mtn_date, mtn_time) 
                    VALUES (
                        :displayName, :name, 
                        :value, :unit, :deviceId,
                        :utc_LAN_received, :utc_cloud_insertion,
                        :mtn_date, :mtn_time
                    )"""), 
                    data_dict
        )
    

    with eng_cloud.begin() as conn:
        conn.execute(
            text("""INSERT INTO boulder.sensor (
                        displayName, name, value, unit, deviceId, 
                        utc_LAN_received, utc_cloud_insertion, 
                        mtn_date, mtn_time) 
                    VALUES (
                        :displayName, :name, 
                        :value, :unit, :deviceId,
                        :utc_LAN_received, :utc_cloud_insertion,
                        :mtn_date, :mtn_time
                    )"""), 
                    data_dict
        )
    

@app.task
def retry_failed_records():
    # TODO: this isn't necessary yet. Leaving stub here in case it's necessary some day
    pass


@worker_init.connect
def make_sqlalchemy_engines(**kwargs):
    """
    This function will run on each worker as soon as that worker starts. This is how
    I make sure my workers are connected to my databases without having to put the
    connection logic within each task that I want to run.
    """
    
    # these apparently do need to be global in order to use them in other tasks
    global eng_cloud  # sqlalchemy db engine connection to cloud database
    global eng_local  # sqlalchemy db engine connection to LAN database
    global apikey     # apikey for weather data
    global lat        # latitude for weather data collection
    global lon        # longitude for weather data collection

    with open('secrets.json', 'r') as f:
        secrets = json.load(f)

    pw_cloud = secrets["cloud_pw"]
    # pw = os.environ.get("TAYLOR_DB_PW")
    eng_cloud = create_engine(f"postgresql+psycopg2://taylor:{pw_cloud}@taylorvananne.com:5432/taylor?sslmode=require", 
        executemany_mode='values_only',
        echo=True, 
        future=True 
    )

    pw_local = secrets["local_pw"]
    # pw = os.environ.get("TAYLOR_DB_PW_LOCAL")
    eng_local = create_engine(f"postgresql+psycopg2://taylor:{pw_local}@localhost:5432/taylor?sslmode=require", 
        executemany_mode='values_only',
        echo=True, 
        future=True 
    )

    # add my weather API key secrets in here as well. This will be my test to see if "global" is required.
    apikey = secrets.get("openweathermap")
    lat    = secrets.get("lat")
    lon    = secrets.get("lon")



# Time-based (periodic) tasks
@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0 * 60.0, get_and_load_weather_data.s())
