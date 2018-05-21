#Import libraries
import jsonpickle
import pandas as pd
import requests
import csv
import json
import bs4
# Set up api for MBTA
MBTA_api = "wX9NwuHnZU2ToO7GmGR9uw"

# make sure I'm in the current directory
import os
os.chdir('/Users/abob/Desktop/github/big-data-spring2018/transit_delays/MBTA_map_new')


#function for parsing json network file to create source target dataframe
sourc_targ_df = pd.DataFrame()

def search(myDict, lookup):
    for key, value in myDict.items():
        if lookup in value:
            return pd.Series(key, value)

#read in origin_dest2 csv with cbd lines removed
with open('data/our_mbta_network.json') as net:
    net_data = json.load(net)

with open('data/our_spider.json') as spid:
    spid_dat = json.load(spid)

with open('data/connect.json') as con:
    con_dat = json.load(con)

len(con_dat)

net_data["parentStops"]

for key, value in data["parentStops"].items():
    if "place-grnst" in value:
        print(key)

##append source ids to sourc targe dataframe
for i in data["links"]:
    s = data["nodes"][i["source"]]["id"]
    source = search(data["parentStops"], s)
    sourc_targ_df = sourc_targ_df.append(source, columns=['source'])

sourc_targ_df2 = pd.DataFrame()
len(data["parentStops"])

##append target ids to sourc targe dataframe
for i in data["links"]:
    s = data["nodes"][i["target"]]["id"]
    source = search(data["parentStops"], s)
    sourc_targ_df2 = sourc_targ_df2.append(source, ignore_index = True)

sourc_targ_fin = pd.concat([sourc_targ_df, sourc_targ_df2], axis = 1)

data["parentStops"].str.contains(data["nodes"][data["links"][0]["source"]]["id"])



print(sourc_targ_fin)


df_source_target = sourc_targ_fin.rename({'0': 'source', '0': 'target'}, axis = 'columns')

sourc_targ_fin.columns
# change column names to reflect the origin and destination stops
df_source_target.columns = ['to_stop', 'from_stop']

print(df_source_target)

# create csv with the origin and destination stops but nothing else
df_source_target.to_csv('source_target.csv')

print (df_source_target)

# read in the file with all the stop info including old id, new id, station name, etc
df_key = pd.read_csv('scripts/data/stops_all.csv')

df_key.head()
# make a smaller dataframe with just the data we need
key_new = df_key[['stop_name_new', 'stop_id_new', 'stop_id_old']].copy()

key_new.head()

# merge the data for the station name and stop id for the destination stop
df_stoppairs = pd.merge(left=df_source_target,right=key_new, left_on='to_stop', right_on='stop_id_new')
# tried to do an inner join to drop additional rows (need to only keep the rows that have values in the
# to_stop' and 'from_stop fields')

# this is too long- must have rows wiht NAN vlaues for to_stop and from_stop
df_stoppairs.shape
df_source_target.shape
print(df_stoppairs)


df_stoppairs.tail()
# dropna didn't seem to work
df_stop_pair2 = df_stoppairs.dropna(axis=0, how='any', subset=['to_stop', 'from_stop'], inplace=False)

df_stop_pair2.shape
# drop duplicates works but only have 114 rows, used to have 116
df_stop_pair2.drop_duplicates(subset=['to_stop', 'from_stop'], inplace = True)
df_stop_pair2.shape

df_stop_pair2.to_csv('MBTA_map_new/stop_list.csv')
