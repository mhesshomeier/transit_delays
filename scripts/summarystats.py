import pandas as pd
import json
import numpy as np
import csv
import os

os.chdir('/Users/meganhess-homeier/github/transit_delays/scripts')

# read in data
df_perf = pd.read_csv('data/mbta_perf_v1.csv')

df_perf.head()

df_perf.origin_name.unique()



df_perf.groupby('origin_id')

df_avg_perf = pd.DataFrame()
avg_time = df_perf.groupby(['origin_id'])['travel_time_sec'].mean()
df_avg_perf = df_avg_perf.append(avg_time)


 # avg_time1 = np.mean(df_perf.travel_time_sec)

df_avg_perf.head()

df_avg_perf = df_avg_perf.transpose()
print(df_avg_perf)
df_avg_perf.head()
df_benchmark = pd.DataFrame()
benchmark = df_perf.groupby(['origin_id'])['benchmark_travel_time_sec'].mean()
benchmark = benchmark.transpose()
benchmark.head()
df_benchmark = benchmark

benchmark = benchmark.to_frame()
df_avg_perf = df_avg_perf.to_frame()

df_avg_perf.index.name='origin_id'

df_avg_perf.head()
benchmark.head()



avg_travel = pd.DataFrame()
avg_travel = pd.merge(df_avg_perf1, benchmark1, how='inner', on="origin_id")

df_avg_perf['origin_id']=df_avg_perf.index
df_avg_perf1 = df_avg_perf.reset_index(drop=True)

benchmark['origin_id']=benchmark.index
benchmark1 = benchmark.reset_index(drop=True)

benchmark1.head()

avg_travel.head()

avg_travel.shape

avg_travel.to_csv('data/avg_benchmark_origin.csv')

avg_travel.head()

avg_travel.append()

stop_id = df_perf.groupby(['origin_id'])['origin_name'].unique()
stop_id.head()



stop_id.to_frame()


stop_id['origin_id']=stop_id.index
stop_id = stop_id.reset_index(drop=False)

stop_id.head()

avg_travel = pd.merge(avg_travel, stop_id, how='inner', on="origin_id")

avg_travel.head()

line_id = df_perf.groupby(['origin_id'])['route_id'].unique()
line_id.head()



line_id.to_frame()


line_id['origin_id']=line_id.index
line_id = line_id.reset_index(drop=False)

line_id.head()

avg_travel = pd.merge(avg_travel, line_id, how='inner', on="origin_id")

avg_travel.head()







avg_travel2 = avg_travel.sort_values('origin_name')

avg_travel2.to_csv('data/avg_benchmark_origin2.csv')

df_demog = pd.read_csv('data/station_demog.csv')

df_demog.shape

# print(avg_time1)
#
# df_avg_perf = pd.DataFrame()
# for index, row in df_perf.origin_id.unique():
#     avg_time = np.mean(df_perf.travel_time_sec)
#     df_avg_perf = df_avg_perf.append(avg_time)
#
# print(avg_time)


df_avg = pd.read_csv('data/avg_benchmark_origin.csv')
