

library(RPostgres)
library(DBI)
library(ggplot2)
library(dplyr)
library(lubridate)
library(plotly)
library(zoo)


# connect to database
con <- dbConnect(drv=Postgres(), dbname="taylor", host="10.0.0.10", port=5432, user="taylor", password="taylor")


# query for our data
df_query <- RPostgres::dbSendQuery(con, "SELECT * FROM boulder.sensor")
df <- dbFetch(df_query)
df$mtn_datetime <- lubridate::ymd_hms(paste0(df$mtn_date, " ", df$mtn_time))


# filter to just temp
dftemp <- df %>% filter(grepl("F", df$unit))


# filter out bad sensor readings, apply a moving average
dftemp <- dftemp %>% 
  filter(value > 40) %>% 
  group_by(displayname) %>% 
  arrange(utc_lan_received) %>% 
  mutate(
    temp_ma = zoo::rollmean(value, k=10, NA)
  )
  

# visualize
gg <- ggplot(dftemp, aes(x=mtn_datetime, y=temp_ma, color=displayname)) +
  geom_step(size=1.1, alpha=0.7) +
  theme_bw()  +
  ggtitle("Apartment Temperature Sensor Readings") +
  labs(x="Datetime (mountain time)", y="Temperature (moving average)") +
  guides(color = guide_legend(override.aes = list(size=2, alpha=1))) 
gg


# plotly vis for fun and interactive exploration
plotly::ggplotly(gg)


# Don't do moving average. plot the real temp
# visualize
gg <- ggplot(dftemp, aes(x=mtn_datetime, y=value, color=displayname)) +
  geom_step(size=1.1, alpha=0.7) +
  theme_bw()  +
  ggtitle("Apartment Temperature Sensor Readings") +
  labs(x="Datetime (mountain time)", y="Temperature (moving average)") +
  guides(color = guide_legend(override.aes = list(size=2, alpha=1))) 
gg


# plotly vis for fun and interactive exploration
plotly::ggplotly(gg)

# 2022-02-16 at some point in early AM, I turned the heat off. temp in free fall.
# 2022-02-16 3:37 PM, closing Ari's door and turning heat back up to normal value.
# I had only turned it up to 70, but hogwarts last reading as of 4:11PM is 73.6




