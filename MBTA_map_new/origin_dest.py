import pandas as pd
import numpy as np
import json
import os
import jsonpickle
from pandas.io.json import json_normalize



os.chdir('/Users/meganhess-homeier/github/transit_delays/MBTA_map_new')

df_network = json.loads('MBTA_map_new.json')


with open ('our_mbta_network.json') as net:
    json.load('MBTA_map_new.json')
