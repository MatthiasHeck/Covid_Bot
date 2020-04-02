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

AUTHOR_ID = 225368082019778560
GITHUB_URL = "https://github.com/MatthiasHeck/Covid_Bot"


WORLD_DATA_URL = "https://covid19api.herokuapp.com/"
WEB_URL = "https://coronavirus.jhu.edu/map.html"

worldData = {}


class Location:
    def __init__(self, confirmed, deaths, recovered):

        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

# track last updated data and dont repopulate if the data is the same


async def populate_world_data():
    r = requests.get(url=WORLD_DATA_URL)
    global worldRawData
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

    return worldRawData


"""async def write_data(data):
    filename = "D:\\Projects\\Python\\Covid_Bot\\DATA_OLD\\" + str(data['DateLastUpdate']) + "_AGE_DATA.TXT"
    if os.path.exists(filename):
        return
    else:
        file_obj = open(filename, 'w')
        # json.loads for reading
        file_obj.write(json.dumps(data))
        file_obj.close()
    return"""


@bot.event
async def on_ready():
    await populate_world_data()
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(help="Reload COVID-19 Data")
async def update(ctx):
    populate_world_data()
    await ctx.send("Data updated as of %s" % worldRawData['updatedAt'])
    return


@bot.command(help="Raw Data")
async def dataurl(ctx):
    await ctx.send(WORLD_DATA_URL)
    return


@bot.command(help="Johns Hopkins Website for COVID-19 tracking")
async def weburl(ctx):
    await ctx.send(WEB_URL)
    return


@bot.command(help="Github for Bot code")
async def github(ctx):
    await ctx.send(GITHUB_URL)
    return


@bot.command(help="Global Information")
async def worldwide(ctx):
    response = "```\n"
    response += "WORLDWIDE COVID-19 DATA_OLD:\n"
    response += "Confirmed: {:,}\n".format(worldRawData['confirmed']['latest'])
    response += "Deaths: {:,}\n".format(worldRawData['deaths']['latest'])
    response += "Recovered: {:,}\n".format(worldRawData['recovered']['latest'])
    response += "```"
    await ctx.send(response)
    return


@bot.command(help="NYI")
async def worldsearch(ctx, *args):

    return


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


bot.run(TOKEN)
