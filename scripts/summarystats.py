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
avg_travel2.shape

df_demog.head()

# try to merge df_demog and avg_travel2 on origin_name and station
avg_demog = pd.merge(avg_travel2, df_demog, how='outer', left_on="origin_id", right_on='STATION')

avg_demog.head()

# use fuzzywuzzy
import fuzzywuzzy

avg_travel2.head()
# check what data type origin name is
avg_travel2['origin_name'].dtype
#try to convert to string
avg_travel2['origin_name'] = avg_travel2['origin_name'].astype('str')

avg_travel2['origin_name'].dtype
# take the brackets off the string
avg_travel2['origin_name'] = avg_travel2['origin_name'].str.strip('[]')


avg_travel2.head()

avg_travel2.shape


# try again to merge the two dataframes, will clean after merge
avg_demog = pd.merge(avg_travel2, df_demog, how='outer', left_on="origin_id", right_on='STATION')

avg_demog.head()

#pull out the records that have missing demographic data (all?)
missing_demog = avg_demog[avg_demog.STATION.isnull()]

missing_demog

from fuzzywuzzy import fuzz

# create a function to match station names
def match_name(name, list_names, min_score=0):
    max_score = -1
    max_name = ''
    for name2 in list_names:
        score = fuzz.ratio(name, name2)
        if (score > min_score) & (score > max_score):
            max_name = name2
            max_score = score
    return (max_name, max_score)
#set up a dictionary to fill and create dataframe
dict_list = []

 # feed my data into the function i created for fuzzy matching
 for name in missing_demog.origin_name:
    match = match_name(name, df_demog.STATION, 15)
    # new dictionary for storing data
    dict_ = {}
    dict_.update({'STATION' : name})
    dict_.update({'match_name' : match[0]})
    dict_.update({'score' : match[1]})
    dict_list.append(dict_)

merge_table = pd.DataFrame(dict_list)
merge_table

# connect my matched names in the merge_table to the avg travel file
avg_withkey = pd.merge(avg_travel2, merge_table, how='inner', left_on="origin_name", right_on='STATION')

avg_withkey.head()
# using the match_name column in the avg_withkey file, connect avg travel time data to demographic data
avg_withdemog = pd.merge(avg_withkey, df_demog, how='inner', left_on="match_name", right_on='STATION')

avg_withdemog.head()
avg_withdemog.shape
# create new column with the % of benchmark travel time
avg_withdemog['percent_over_benchmark'] = avg_withdemog.travel_time_sec / avg_withdemog.benchmark_travel_time_sec

avg_withdemog.head()

# export the full file to csv!
avg_withdemog.to_csv('data/joined_avgtravel_demographics_percent.csv')

# create dataframes that organize all this data by color line

# travel_demographics_red = pd.DataFrame(avg_withdemog['LINE'] == 'RED')
travel_demographics_red = pd.DataFrame
travel_demographics_red = avg_withdemog[(avg_withdemog['LINE'] == 'RED')]
travel_demographics_red.head()

# export to CSV
travel_demographics_red.to_csv('data/travel_demographics_red.csv')

# do it for the blue line
travel_demographics_blue = pd.DataFrame
travel_demographics_blue = avg_withdemog[(avg_withdemog['LINE'] == 'BLUE')]
travel_demographics_blue.head()

# export to CSV
travel_demographics_blue.to_csv('data/travel_demographics_blue.csv')

# do it for the green line
travel_demographics_green = pd.DataFrame
travel_demographics_green = avg_withdemog[(avg_withdemog['LINE'] == 'GREEN')]
travel_demographics_green.head()

# export to CSV
travel_demographics_green.to_csv('data/travel_demographics_green.csv')

# do it for the orange line
travel_demographics_orange = pd.DataFrame
travel_demographics_orange = avg_withdemog[(avg_withdemog['LINE'] == 'ORANGE')]
travel_demographics_orange.head()

# export to CSV
travel_demographics_orange.to_csv('data/travel_demographics_orange.csv')



#read in the red line demographics and travel data
df_red = pd.read_csv('data/travel_demographics_red.csv')

df_red.head()

# create a dataframe with only the columns I really need
df_red_subset = df_red[['origin_name','med_incom','percent_over_benchmark']].copy()
df_red_subset.head()

# read it out to CSV
df_red_subset.to_csv('data/red_bar_data.csv')


# if fuzzywuzzy.ratio(avg_travel2.origin_id(['origin_id']), df_demog.STATION(['STATION'])) >= 97
    # avg_demog1 = pd.merge(avg_travel2, df_demog, how='outer', left_on="origin_id", right_on='STATION')
    # return(avg_demog1)


# print(avg_time1)
#
# df_avg_perf = pd.DataFrame()
# for index, row in df_perf.origin_id.unique():
#     avg_time = np.mean(df_perf.travel_time_sec)
#     df_avg_perf = df_avg_perf.append(avg_time)
#
# print(avg_time)


# df_avg = pd.read_csv('data/avg_benchmark_origin.csv')
