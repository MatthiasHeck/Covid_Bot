import requests
import datetime
import pytz

ageURL = "https://maps.ct.gov/arcgis/rest/services/Hosted/CT_COVID19/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=50"
countyURL = "https://maps.ct.gov/arcgis/rest/services/Hosted/CT_COVID19/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=1000"

#r = requests.get(url=countyURL)
#rawdata = r.json()
#data = rawdata['features']

dataByAge = {}

r = requests.get(url=ageURL)
rawdata = r.json()
data = rawdata['features'][0]['attributes']

for d in data:
    dataByAge[d] = data[d]

print('end')
