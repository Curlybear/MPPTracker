import configparser
import csv
import requests
import json
from collections import OrderedDict
import os

# Config reader
dir = os.path.dirname(__file__)
filename = os.path.join(dir, 'config.ini')
config = configparser.ConfigParser()
config.read(filename)

# API Key
apiKey = config['DEFAULT']['api_key']

convertIDs = {}
convertNames = {}
with open("countries.csv", "r", encoding="latin-1") as f:
    for row in csv.reader(f, delimiter=',', skipinitialspace=True):
        convertIDs[row[0]] = row[2]
        convertNames[row[0]] = row[1]

r = requests.get('https://api.erepublik-deutschland.de/' + apiKey + '/countries/details/all')
obj = json.loads(r.text, object_pairs_hook=OrderedDict)

nodes_dict = []
links_dict = []

for country in obj['countries']:
    nodes_dict.append({"name": convertNames[country],
                       "group": str(obj['countries'][country]['military']['alliance'])})

    mpps = obj['countries'][country]['military']['mpps']
    if mpps:
        for mpp in mpps:
            links_dict.append({"source": convertIDs[str(country)],
                               "target": convertIDs[str(mpp['country_id'])],
                               "value": 1})
    else:
        links_dict.append({"source": convertIDs[str(country)],
                           "target": convertIDs[str(country)],
                           "value": 1})

data_dict = {"nodes": nodes_dict,
             "links": links_dict}

f = open('data.json', 'wt', encoding='utf-8')
f.write(json.dumps(data_dict))
f.close()
