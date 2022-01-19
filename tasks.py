

# this is essentially what I'm attempting..
# https://stackoverflow.com/questions/14526249/celery-worker-database-connection-pooling


from my_celery_app import app
from celery.signals import worker_init
from sqlalchemy import create_engine, text
import json
# import os


@app.task
def load_sensor(data_dict):
    #TODO: I want to pass in my own JSON that represents the record to add to database.
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
    # TODO: if I feel like this is necessary...
    pass


@worker_init.connect
def make_sqlalchemy_engines(**kwargs):
    
    with open('secrets.json', 'r') as f:
        secrets = json.load(f)

    pw_cloud = secrets["cloud_pw"]
    # pw = os.environ.get("TAYLOR_DB_PW")
    global eng_cloud
    eng_cloud = create_engine(f"postgresql+psycopg2://taylor:{pw_cloud}@taylorvananne.com:5432/taylor?sslmode=require", 
        executemany_mode='values_only',
        echo=True, 
        future=True 
    )

    pw_local = secrets["local_pw"]
    # pw = os.environ.get("TAYLOR_DB_PW_LOCAL")
    global eng_local
    eng_local = create_engine(f"postgresql+psycopg2://taylor:{pw_local}@localhost:5432/taylor?sslmode=require", 
        executemany_mode='values_only',
        echo=True, 
        future=True 
    )


# TODO: I haven't really implemented my retry_failed_records() task yet, might come back to that...
@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0 * 60.0, retry_failed_records.s())
