import pandas as pd
import numpy as np


df_stops2016 = pd.read_csv("data/stops_2016.txt")
df_stops2016.head()


df_stopscurrent = pd.read_csv("data/stops_current.txt")
df_stopscurrent.head()


stops_all = pd.merge(df_stops2016, df_stopscurrent, how='outer', on=["stop_lat", "stop_lon"],
         left_index=False, right_index=False, sort=False,
         suffixes=('_old', '_new'), copy=True, indicator=False,
         validate=None)

stops_all.head()

stops_all.to_csv('data/stops_all.csv')


df_spider_all = pd.read_json('data/spider_all.json')
df_spider_green = pd.read_json('data/spider_green.json')

df_spider_all.head()


df_spider = pd.concat([df_spider_all, df_spider_green], axis = 1, verify_integrity =False, copy = False)

df_spider.head()

df_spider_clean2 = df_spider.loc[:,~df_spider.columns.duplicated()]

# df_spider_clean = np.unique(df_spider.columns, return_index=True)

df_spider_clean2.head()


df_spider_clean2.to_json('data/spider_allgreen.json')
