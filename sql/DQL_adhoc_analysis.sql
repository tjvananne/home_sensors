


-- grab most recent records; make sure we're receiving data
-- this works on both LAN and Cloud databases
select * from boulder.sensor
order by utc_lan_received desc
limit 50;



