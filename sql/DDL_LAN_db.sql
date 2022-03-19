
-- LAN database DDL

    CREATE TABLE boulder.sensor (
        displayName         varchar(40),
        name                varchar(30),
        value               float4,
        unit                varchar(15),
        deviceId            int2,
        utc_LAN_received    varchar(27),
        utc_cloud_insertion varchar(27),
        mtn_date            date,
        mtn_time            time
    );
