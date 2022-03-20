
-- Note: Storage isn't really an issue on my LAN server.
-- I'm going to create both JSON and JSONb fields so I can test them both out.

    CREATE TABLE boulder.weather_raw (
        weather_json_raw    json,
        weather_jsonb       jsonb,
        utc_ts              varchar(27),
        mtn_date            date,
        mtn_time            time
    );


-- detailed weather data

    CREATE TABLE boulder.weather (
        id                  int4 not null,
        lon                 varchar(14),
        lat                 varchar(14),
        weather_desc        varchar(30),
        temp                decimal(6, 3),
        temp_feels_like     decimal(6, 3),
        temp_min            decimal(6, 3),
        temp_max            decimal(6, 3),
        pressure            int4,
        humidity            int4,
        visibility          int4,
        wind_speed          decimal(6, 3),
        wind_deg            int2,
        clouds_all          varchar(10),
        utc_ts              varchar(27),
        mtn_date            date,
        mtn_time            time,
        dt                  varchar(11),
        dt_sunrise          varchar(11),
        dt_sunset           varchar(11),
        timezone            varchar(8)
    );


