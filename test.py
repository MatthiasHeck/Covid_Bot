import requests
import datetime
import pytz

WORLD_DATA_URL = "https://covid19api.herokuapp.com/"


worldData = {}
worldRawData = ""
worldDeathsData = {}


class Location:
    def __init__(self, confirmed, deaths, recovered):

        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered


# track last updated data and dont repopulate if the data is the same

r = requests.get(url=WORLD_DATA_URL)
worldRawData = r.json()


for d in worldRawData['confirmed']['locations']:
    loc = Location(d['latest'], 0, 'nan')
    worldData[(d['country'], d['province'])] = loc

for d in worldRawData['deaths']['locations']:
    worldData[(d['country'], d['province'])].deaths = d['latest']

for d in worldRawData['recovered']['locations']:
    try:
        worldData[(d['country'], d['province'])].recovered = d['latest']
    except:
        continue

response = "```\n"
response += "WORLDWIDE COVID-19 DATA_OLD:\n"
response += "Confirmed: {:,}\n".format(worldRawData['confirmed']['latest'])
response += "Deaths: {:,}\n".format(worldRawData['deaths']['latest'])
response += "Recovered: {:,}\n".format(worldRawData['recovered']['latest'])
response += "```"


print('end')
