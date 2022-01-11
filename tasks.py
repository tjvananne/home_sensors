

# this is essentially what I'm attempting..
# https://stackoverflow.com/questions/14526249/celery-worker-database-connection-pooling


from my_celery_app import app
import time
import os
from celery.signals import worker_init
from sqlalchemy import create_engine, text


@app.task
def load_sensor():
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
                    )"""), {
                        "displayName": "test_room",
                        "name": "test_name",
                        "value": 42,
                        "unit": "test_unit",
                        "deviceId": 3,
                        "utc_LAN_received": "2022-01-02 08:58:59",
                        "utc_cloud_insertion": "2022-01-02 08:58:59",
                        "mtn_date": "2022-01-02",
                        "mtn_time": "08:58:59"
                    }
        )
    



@worker_init.connect
def make_sqlalchemy_engines(**kwargs):
    
    # TODO: test if "global" is necessary.
    # I believe these workers are all separate processes. Global shouldn't work
    # across processes. So they should be "global" within each worker? That's my hope at least.
    pw = os.environ.get("TAYLOR_DB_PW")
    global eng_cloud
    eng_cloud = create_engine(f"postgresql+psycopg2://taylor:{pw}@taylorvananne.com:5432/taylor?sslmode=require", 
        executemany_mode='values_only',
        echo=True, 
        future=True 
    )

    pw = os.environ.get("TAYLOR_DB_PW_LOCAL")
    global eng_local
    eng_local = create_engine(f"postgresql+psycopg2://taylor:{pw}@localhost:5432/taylor?sslmode=require", 
        executemany_mode='values_only',
        echo=True, 
        future=True 
    )



# I'm fairly certain it's fine to put this here? Not 100% sure if that is where it belongs
@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, load_sensor.s())
