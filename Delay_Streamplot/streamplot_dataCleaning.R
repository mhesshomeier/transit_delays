##### MBTA Performance data cleaning #######

library(dplyr)

setwd("/Users/abob/Desktop/github/big-data-spring2018/transit_delays/gtfs_scrape")

mbta_perf = read.csv("mbta_perf_v3.csv")
#remove data with 0 benchmark time
new_perf = subset(mbta_perf, benchmark_travel_time_sec > 0)

#Convert to percent of benchmark
new_perf$pct_of_benchmark = new_perf$travel_time_sec/new_perf$benchmark_travel_time_sec

#Convert Unix time to datetime
new_perf$datetime = as.POSIXct(as.numeric(new_perf$dep_dt), origin = '1970-01-01', tz = 'EST')

#Remove data from night before
mbta_per = subset(new_perf, datetime > as.POSIXct("2017-12-28 01:46:00"))

#Create column for 15 minute bucket in which departure fails
mbta_per$dep_time_by15 = cut(mbta_per$datetime, breaks="15 min")

#Group by route_id and departure time bucket and summarize avg. pct of benchmark for each
avg_pct_benchmark = mbta_per %>% 
  group_by_(.dots=c("route_id","dep_time_by15")) %>% 
  summarize(avg_pct_benchmark=mean(pct_of_benchmark))

avg_pct_benchmark2 = subset(avg_pct_benchmark, dep_time_by15 != "2017-12-28 04:59:00" & dep_time_by15 != "2017-12-28 23:59:00")

write.csv(avg_pct_benchmark2, file = "avg_pct_benchmark.csv")

#Groupby origin_name and dep_time bucket and summarize avg. pct of benchmark for each

Orig_pct_bench = mbta_per %>% 
  group_by_(.dots=c("origin_name","dep_time_by15")) %>% 
  summarize(avg_pct_benchmark=mean(pct_of_benchmark))

Orig_pct_bench2 = subset(Orig_pct_bench, dep_time_by15 == "2017-12-28 08:29:00")

perf_eight = subset(mbta_per, dep_time_by15 == "2017-12-28 08:29:00")

dist_eight = distinct(perf_eight, origin_name, .keep_all = T)

Orig_pct_bench3 = inner_join(Orig_pct_bench2, dist_eight, by = "origin_name")

stops = read.csv("stops.csv")

Orig_pct_bench3$orig_name_old = stops$parent_station[match(Orig_pct_bench3$origin_id, stops$stop_code)]

Orig_pct_bench3$dest_name_old = stops$parent_station[match(Orig_pct_bench3$dest_id, stops$stop_code)]

Orig_pct_bench3$link = paste(Orig_pct_bench3$orig_name_old, Orig_pct_bench3$dest_name_old, sep = "|")