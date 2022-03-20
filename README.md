# home_sensors

My personal project for collecting, processing, storing the sensor data I'm collecting in my home.

- [celery/dockercompose/sqlalchemy](https://stackoverflow.com/questions/55766653/docker-compose-bind-celery-to-postgres-database)


## Celery Tasks

- Loading hubitat temp data into databases:
  - hubitat is configured to send data to my LAN server's `/sensor` flask route which calls `receive_sensor_data()`
  - `load_sensor()` celery task is called from the above route
- Pull / load public weather data:
  - Won't have anything to do with flask, just a timed (periodic) celery task


## Docker Compose Notes

* **must be in the directory where the `docker-compose.yml` file is for the following commands**
* To rebuild the docker-compose containers: `sudo docker-compose build` 
* To check if your docker compose is running, you run `sudo docker-compose ps`
* Spin up the docker-compose, `sudo docker-compose up -d` (`-d` puts it in the background). I also have a systemd service file that starts this up automatically in the event the server reboots.
* [this is a great resource](https://blog.deepjyoti30.dev/celery_compose) about configuring celery and rabbitmq


## Hubitat notes

1. Using the Maker API app within hubitat, we can either push data to our LAN device at a dedicated IP, or I can poll endpoints continuously from my LAN device to my hubitat. I think it's a little cleaner to push the data instead of poll for it. That's the direction I'm taking for now.


## Dev environment and deploying

It quickly became too much work to maintain my virtual box VM and keep that in-sync with the resources installed on my LAN server. So now I'm treating my LAN server as my development server.

When adding more functionality in the future:

1. make sure `./transfer_files_to_server.sh` is pushing all the files my LAN server will need
2. update all of the `.dockerfile`s to make sure they all have the right files, dependencies, etc
3. run `./transfer_files_to_server.sh`, ssh into the LAN server, navigate to the project directory, execute `sudo docker-compose up -d` 
  - omit the `-d` if you want to read the logs as data is passing through the system - useful for testing/debugging


## Testing

To run tests (there's only a handful of tests for utils currently):

```
$ pytest -rA
```


## Docker compose logs

[This stack overflow answer](https://stackoverflow.com/a/40721348/3586093) has good info on inspecting logs of a running docker compose environment
