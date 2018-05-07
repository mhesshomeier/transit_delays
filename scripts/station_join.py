import pandas as pd
import numpy as np
import json
import os


# Important take-aways:

# File with both current and old station_ids is 'stops_all.csv', columns from the old file
# are labeled _old, columns from the new file are labeled _new

# combined spider file with both the old stops and green line stops is saved as 'spider_allgreen.json'
# combined station network file with both old stations and green line stations is saved as 'station_allgreen.json'


# read in old stops data and check it out
df_stops2016 = pd.read_csv("data/stops_2016.txt")
df_stops2016.head()

# read in new stops data and check it out
df_stopscurrent = pd.read_csv("data/stops_current.txt")
df_stopscurrent.head()

# merge the old and new stops data on columns 'stop_lat' and 'stop lon', old columns named with Convention
# _old, columns from the new stops file named with convention _new
stops_all = pd.merge(df_stops2016, df_stopscurrent, how='outer', on=["stop_lat", "stop_lon"],
         left_index=False, right_index=False, sort=False,
         suffixes=('_old', '_new'), copy=True, indicator=False,
         validate=None)
# check it out
stops_all.head()
# read the combined data to a CSV
stops_all.to_csv('data/stops_all.csv')

# Read in the spider data as dataframes, all stations and green line stations
df_spider_all = pd.read_json('data/spider_all.json')
df_spider_green = pd.read_json('data/spider_green.json')
# check it out
df_spider_all.head()

# merge the two data frames
df_spider = pd.concat([df_spider_all, df_spider_green], axis = 1, verify_integrity =False, copy = False)
# check it out
df_spider.head()
# drop duplicates
df_spider_clean2 = df_spider.loc[:,~df_spider.columns.duplicated()]


# df_spider_clean = np.unique(df_spider.columns, return_index=True) (this didn't work)
# Check out the de-duplicated dataframe
df_spider_clean2.head()

# read the new, clean, combined data frame to a json
df_spider_clean2.to_json('data/spider_allgreen.json')

# load in the station network data
# df_station_all = pd.read_json('data/station-network_all.json')
# df_station_green = pd.read_json('data/station-network_green.json') (didn't work because
# the arrays are different lengths, not a clean dataframe, need to load in as dictionary then convert to a datafram)

# Load station network jsons as dictionaries
with open('data/station-network_all.json') as json_data:
    data_all = json.load(json_data)
with open('data/station-network_green.json') as json_data1:
    data_green = json.load(json_data1)
# check it out
print(data_all)
print(data_green)

# put the station network dictionary into a dataframe, oriented by index
df_station_all = pd.DataFrame.from_dict(data_all, orient = 'index')
# check it out
print(df_station_all)
# put the green station network into a dataframe, oriented by index
df_station_green = pd.DataFrame.from_dict(data_green, orient='index')
# combine the two station network dataframes
df_station = pd.concat([df_station_all, df_station_green], axis = 1, verify_integrity =False, copy = False)
# Drop the duplicated stations
df_station_clean = df_station.loc[:,~df_station.columns.duplicated()]
# check it out
df_station_clean.head()
# read that dataframe to one comprehensive json
df_station_clean.to_json('data/station_allgreen.json')
