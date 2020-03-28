import requests
import datetime
import pytz

ageURL = "https://maps.ct.gov/arcgis/rest/services/CT_DPH_COVID_19_PROD_Layers/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=50"
countyURL = "https://maps.ct.gov/arcgis/rest/services/CT_DPH_COVID_19_PROD_Layers/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=2000"

dataByCounty = {}

r = requests.get(url=countyURL)
rawdata = r.json()
data = rawdata['features']

for i in range(0, data.__len__()):
    dataByCounty[data[i]['attributes']['COUNTY']] = data[i]['attributes']




dataByAge = {}

r = requests.get(url=ageURL)
rawdata = r.json()
data = rawdata['features'][0]['attributes']

for d in data:
    dataByAge[d] = data[d]

print('end')
