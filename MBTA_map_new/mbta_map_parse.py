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
            return pd.Series(key)

#read in origin_dest2 csv with cbd lines removed
with open('our_mbta_network.json') as net:
    data = json.load(net)

for key, value in data["parentStops"].items():
    if "place-grnst" in value:
        print(key)

##append source ids to sourc targe dataframe
for i in data["links"]:
    s = data["nodes"][i["source"]]["id"]
    source = search(data["parentStops"], s)
    sourc_targ_df = sourc_targ_df.append(source, ignore_index = True)

sourc_targ_df2 = pd.DataFrame()
len(data["parentStops"])

##append target ids to sourc targe dataframe
for i in data["links"]:
    s = data["nodes"][i["target"]]["id"]
    source = search(data["parentStops"], s)
    sourc_targ_df2 = sourc_targ_df2.append(source, ignore_index = True)

sourc_targ_fin = pd.concat([sourc_targ_df, sourc_targ_df2], axis = 1)

data["parentStops"].str.contains(data["nodes"][data["links"][0]["source"]]["id"])
