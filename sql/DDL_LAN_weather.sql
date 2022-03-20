
-- Note: Storage isn't really an issue on my LAN server.
-- I'm going to create both JSON and JSONb fields so I can test them both out.

    CREATE TABLE boulder.weather_raw (
        weather_json_raw    json,
        weather_jsonb       jsonb,
        utc_ts              varchar(27),
        mtn_date            date,
        mtn_time            time
    );


