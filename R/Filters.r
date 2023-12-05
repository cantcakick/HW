hotel_bookings <- read.csv("hotel_bookings.csv")
head(hotel_bookings)
colnames(hotel_bookings)
install.packages('ggplot2')
library(ggplot2)
ggplot(data = hotel_bookings) +
  geom_point(mapping = aes(x = lead_time, y = children))
ggplot(data = hotel_bookings) +
  geom_bar(mapping = aes(x = hotel, fill = market_segment))
ggplot(data = hotel_bookings) +
  geom_bar(mapping = aes(x = hotel)) +
  facet_wrap(~market_segment)
install.packages('tidyverse')
library(tidyverse)
onlineta_city_hotels <- filter(hotel_bookings, #assign a filter to onlineta_city_hotels to create a new data frame
                           (hotel=="City Hotel" & #filter hotel type City Hotel & booking type from the marketing_segment Online TA
                             hotel_bookings$market_segment=="Online TA"))
View(onlineta_city_hotels)
#This can also be done with the pipe operator %>% 
onlineta_city_hotels_v2 <- hotel_bookings %>%
  filter(hotel=="City Hotel") %>%
  filter(market_segment=="Online TA")

ggplot(data = onlineta_city_hotels) +
  geom_point(mapping = aes(x = lead_time, y = children))

geom_jitter() # makes it easier to see overlapping data points 