####Add information to origin destination datatable

setwd("/Users/abob/Desktop/github/big-data-spring2018/transit_delays/gtfs_scrape")
stops = read.csv("stops.csv")
s_t = read.csv("to_from.csv")
colnames(s_t)


s_stops = merge(s_t, stops, by.x = "from_stop", by.y = "stop_id")
s_stops = select(s_stops, from_stop, to_stop, from.stop.code = stop_code, from.stop.name = stop_name, from.stop.desc = stop_desc, from.parent.stat = parent_station)

st_stops = merge(s_stops, stops, by.x = "to_stop", by.y = "stop_id")
st_stops = select(st_stops, from_stop, to_stop, from.stop.code, from.stop.name, from.stop.desc, from.parent.stat, to.stop.code = stop_code, to.stop.name = stop_name, to.stop.desc = stop_desc, to.parent.stat = parent_station)

write.csv(st_stops, file = "Mbta_stat_links.csv")

mbta_perf = read.csv("mbta_perf_v3.csv")
summary(mbta_perf)
dim(mbta_perf)
length(unique(mbta_perf$dest_name))
length(unique(mbta_perf$origin_name))

perf2 = read.csv("mbta_perf_v2.csv")
dim(perf2)


