##### MBTA Performance data cleaning #######

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


write.csv(avg_pct_benchmark, file = "avg_pct_benchmark.csv")