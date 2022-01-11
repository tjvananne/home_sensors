# home_sensors
My personal project for collecting, processing, storing the sensor data I'm collecting in my home.

## Dev environment startup

Pre-flight checklist for my dev environment:

* VirtualBox ubuntu 20.04 server is running
* Postgresql is up on the vbox (I've enabled this service, should start on boot up)
* Start the rabbitmq docker container (TODO: make this start up on boot up)
    - On vbox server: `sudo docker container start nostalgic_hermann` (I forgot to name it so it gave my container this default name)
* Start celery worker
    - On development machine: `celery -A my_celery_app worker --pool=eventlet --loglevel=INFO`
        - the `--pool=eventlet` is because Windows can't run the native pool type... it isn't cross platform. But eventlet is super easy to install, so it's a big whatever.
* Start celery beat
    - On development machine: `celery -A my_celery_app beat --loglevel=INFO`
        - Mental model for beat: consider this like your application that is sending tasks to be executed (flask, in my case). Celery beat is simply a scheduler that sends the tasks to your worker(s). Celery beat does not execute tasks itself.




## Database thoughts:

So I need two database connections in SQL Alchemy:

1) Cloud database running Postgresql 14
2) Local (zenbook) database running Postgresql 14

Pre-Algorithm:

1. DDL on Cloud database (boulder_sensor table)
1. DDL on local database (boulder_sensor and boulder_sensor_fail tables)

Algorithm:

1. create the timestamp upon receipt of the JSON data; populate this timestamp into two separate fields
1. enrich the data with additional fields
1. convert the data to pandas data frame
1. check boulder_sensor_fail table
    1. if it has contents, append those out into data frame and update timestamp2 value on these records
    1. if no contents, then simply continue to next step
1. Attempt to write the record to the cloud database
    1. if unsuccessful, write *only the new* record to the sensor_fail local database table
    1. if successful, write the record to the sensor local database table *and truncate the sensor_fail table*


## Next steps

Try creating my SQLAlchemy engines (`global`) on the worker init signal in Celery. If that doesn't work, then just use Pika / RabbitMQ or maybe just Redis?




