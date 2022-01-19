# home_sensors
My personal project for collecting, processing, storing the sensor data I'm collecting in my home.

- [celery/dockercompose/sqlalchemy](https://stackoverflow.com/questions/55766653/docker-compose-bind-celery-to-postgres-database)

## Bookmark:

* I'm trying to figure out how to get secrets into my celery workers... 
  - It looks like I'm not able to read them from my secrets.json file
  - It does look like it works if I use environment variables from host machine, but not sure what this would look like in docker-compose...


## Docker notes

Set up flask docker container:

* `taylor@zenbook:~/home_sensors$ sudo docker build -t homesensor_flask -f Flask.dockerfile .`
* `taylor@zenbook:~/home_sensors$ sudo docker run -d --name myflask_sensor homesensor_flask`

Set up rabbitmq (no dockerfile, just using the base image):

* `taylor@zenbook:~/home_sensors$ sudo docker run -d -p 5672:5672 rabbitmq`

Set up celery docker container:

* `taylor@zenbook:~/home_sensors$ sudo docker build -t homesensor_celery -f Celery.dockerfile .`
* `taylor@zenbook:~/home_sensors$ sudo docker run -d --name mycelery_sensor homesensor_celery`


**Docker Compose Notes**:

* [this is a great resource](https://blog.deepjyoti30.dev/celery_compose) about configuring celery and rabbitmq

```yaml
# THIS IS NOT MY COMPOSE FILE, it's just an example from the site above
version: "3.7"

services:
  # Deploy the broker.
  rabbitmq_server:
    image: rabbitmq:3-management
    ports:
      # Expose the port for the worker to add/get tasks
      - 5672:5672
      # OPTIONAL: Expose the GUI port
      - 15672:15672

  # Deploy the worker
  worker:
    # Build using the worker Dockerfile
    build:
      context: .
      dockerfile: worker.Dockerfile
    # Need to access the database
    # OPTIONAL: If you worker needs to access your db that is deployed
    # locally, then make the network mode as host.
    network_mode: host
    # Pass the rabbitmq_uri as env varible in order to
    # connect to our service
    environment:
      # NOTE: Below we are using 127.0.0.1 because this container
      # will run on the host network, thus it will have access to the
      # host network.
      # If it would not have run locally, we would have had to
      # connect using the service name like following:
      # amqp:rabbitmq_server:5672
      rabbitmq_uri: amqp://127.0.0.1:5672
    # Make it wait for rabbitmq deployment
    depends_on: 
      - rabbitmq_server
```


The answer here was the network mode I was using as well as the rabbitmq_uri environment setting.

## hubitat notes:

1. Using the Maker API app within hubitat, we can either push data to our LAN device at a dedicated IP, or I can poll endpoints continuously from my LAN device to my hubitat. I think it's a little cleaner to push the data instead of poll for it. That's the direction I'm taking for now.


## Next steps

1. 


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




