import os
import requests
import json

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', case_insensitive=True)

CHANNEL_ID = 692781692913582190
# CHANNEL_ID = 692787370570940438

DATA_AGE = ""
DATA_AGE_TEMP = ""
DATA_URL = "https://maps.ct.gov/portal/apps/opsdashboard/index.html#/48d54b859c8b4a8e87a0376af3513140"
AUTHOR_ID = 225368082019778560
GITHUB_URL = "https://github.com/MatthiasHeck/Covid_Bot"

# CT Case by County
# https://maps.ct.gov/arcgis/rest/services/Hosted/CT_COVID19/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=1000

# CT by Age
# https://maps.ct.gov/arcgis/rest/services/Hosted/CT_COVID19/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=50

ageURL = "https://maps.ct.gov/arcgis/rest/services/CT_DPH_COVID_19_PROD_Layers/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=50"
countyURL = "https://maps.ct.gov/arcgis/rest/services/CT_DPH_COVID_19_PROD_Layers/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=2000"

dataByAge = {}
dataByCounty = {}


def isValidChannel(ctx):
    if ctx.channel.id == CHANNEL_ID:
        return True
    else:
        return False


# track last updated data and dont repopulate if the data is the same
async def populate_age_data():
    r = requests.get(url=ageURL)
    rawdata = r.json()
    data = rawdata['features'][0]['attributes']

    for d in data:
        dataByAge[d] = data[d]

    await write_age_data(dataByAge)
    return


async def write_age_data(data):
    filename = "D:\\Projects\\Python\\Covid_Bot\\DATA\\" + str(data['DateLastUpdate']) + "_AGE_DATA.TXT"
    if os.path.exists(filename):
        return
    else:
        file_obj = open(filename, 'w')
        # json.loads for reading
        file_obj.write(json.dumps(data))
        file_obj.close()
    return


async def populate_county_data():
    r = requests.get(url=countyURL)
    rawdata = r.json()
    data = rawdata['features']

    for i in range(0, data.__len__()):
        dataByCounty[data[i]['attributes']['COUNTY']] = data[i]['attributes']

    await write_county_data(dataByCounty)
    return


async def write_county_data(data):
    filename = "D:\\Projects\\Python\\Covid_Bot\\DATA\\" + str(data['Tolland']['DateLastUpdated']) + "_COUNTY_DATA.TXT"
    if os.path.exists(filename):
        return
    else:
        file_obj = open(filename, 'w')
        # json.loads for reading
        file_obj.write(json.dumps(data))
        file_obj.close()
    return


async def getDataAge():
    r = requests.get(url=countyURL)
    rawdata = r.json()
    data = rawdata['features']

    DATA_AGE_TEMP = data[0]['attributes']['DateLastUpdated']

    return DATA_AGE_TEMP


async def setDataAge(thisAge):
    DATA_AGE = thisAge
    return


@bot.event
async def on_ready():
    await setDataAge(await getDataAge())
    await populate_age_data()
    await populate_county_data()
    print(f'{bot.user.name} has connected to Discord!')

    # channel = bot.get_channel(CHANNEL_ID)
    # await channel.send("Beep Boop")


@bot.command(help="Reload COVID-19 Data")
async def update(ctx):
    if DATA_AGE is None or DATA_AGE == (await getDataAge()):
        await populate_age_data()
        await populate_county_data()
        await ctx.send("`\nData reloaded`")
    else:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send("Data is already up to date.")
    return


@bot.command(help="Full Statistics")
async def fullinfo(ctx):
    response = '```' \
               'Confirmed Cases: %s\n' \
               'Hospitalized: %s\n' \
               'Deaths: %s\n' \
               'Recovered: %s\n' \
               '```' % (
                   dataByAge['ConfirmedCases'], dataByAge['HospitalizedCases'], dataByAge['Deaths'],
                   dataByAge['Recovered'])
    await ctx.send(response)
    return


@bot.command(help="List the number of confirmed COVID-19 cases")
async def confirmed(ctx):
    response = '`\nConfirmed COVID-19 Cases: %s`' % (dataByAge['ConfirmedCases'])
    await ctx.send(response)
    return


@bot.command(help="Number of hospitalized cases")
async def hospital(ctx):
    response = '`\nHospitalized Cases: %s`' % (dataByAge['HospitalizedCases'])
    await ctx.send(response)
    return


@bot.command(help="Number of confirmed deaths by COVID-19")
async def deaths(ctx):
    response = '`\nConfirmed Deaths: %s`' % (dataByAge['Deaths'])
    await ctx.send(response)
    return


@bot.command(help="Number of recoveries")
async def recovered(ctx):
    response = '`\nCases Recovered: %s`' % (dataByAge['Recovered'])
    await ctx.send(response)
    return


ageranges = {
    **dict.fromkeys(range(0, 10), ['Cases_age0_9', 'Ages 0-9']),
    **dict.fromkeys(range(10, 20), ['Cases_age10_19', 'Ages 10-19']),
    **dict.fromkeys(range(20, 30), ['Cases_age20_29', 'Ages 20-29']),
    **dict.fromkeys(range(30, 40), ['Cases_age30_39', 'Ages 30-39']),
    **dict.fromkeys(range(40, 50), ['Cases_age40_49', 'Ages 40-49']),
    **dict.fromkeys(range(50, 60), ['Cases_age50_59', 'Ages 50-59']),
    **dict.fromkeys(range(60, 70), ['Cases_age60_69', 'Ages 60-69']),
    **dict.fromkeys(range(70, 80), ['Cases_age70_79', 'Ages 70-79']),
    **dict.fromkeys(range(80, 101), ['Cases_age80_Older', 'Ages 80 and older'])
}


@bot.command(help="List number of cases by age group (0-100)")
async def age(ctx, *arg):
    if arg.__len__() != 1:
        await ctx.send("`\nAge must be a number between 0-100`")
        return

    try:
        if 100 >= int(arg[0]) >= 0:
            response = "`\nNumber of cases for %s: %s`" % (
                ageranges[int(arg[0])][1], dataByAge[ageranges[int(arg[0])][0]])
        else:
            response = "`\nAge must be a number between 0-100`"
    except:
        response = "`\nAge must be a number between 0-100`"

    await ctx.send(response)
    return


@bot.command()
async def url(ctx):
    await ctx.send(DATA_URL)
    return


@bot.command(help="List COVID-19 cases by county")
async def county(ctx, *arg):
    if 2 < arg.__len__() == 0:
        response = "```\n"
        response += "\n1".join(dataByCounty.keys())
        response += "```"
        await ctx.send(response)
        return

    try:
        if arg.__len__() == 2:
            county = arg[0].title() + " " + arg[1].title()
        else:
            county = arg[0].title()

        d = dataByCounty[county]

        response = "```\n"
        response += "%s County\nConfirmed Cases: %s\nHospitalized: %s\nDeaths:%s" % \
                    (d['COUNTY'], d['ConfirmedCases'], d['HospitalizedCases'], d['Deaths'])
        response += "```"
    except:
        response = "```\n"
        response += "\n".join(dataByCounty.keys())
        response += "```"

    await ctx.send(response)
    return


@bot.command(help='NYI :: Display the new cases since the last data')
async def newcases(ctx):

    return


@bot.command()
async def github(ctx):
    await ctx.send(GITHUB_URL)
    return


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


bot.run(TOKEN)
