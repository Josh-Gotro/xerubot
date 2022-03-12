import urllib.parse
import urllib.request
import re
import random
import giphy_client
import os

from discord.ext import commands
from data import general
from discord.utils import get
from giphy_client.rest import ApiException

if not os.environ.get('TOKEN'):
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv('TOKEN')
    apiKey = os.getenv("API_KEY")
    myID = os.getenv("MY_DISCORD_ID")
else:
    token = os.environ.get('TOKEN')
    apiKey = os.environ.get("API_KEY")
    myID = os.environ.get("MY_DISCORD_ID")


async def youtube(ctx, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})',
                                htm_content.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])


async def giphy(ctx, query):
    api_instance = giphy_client.DefaultApi()
    try:
        response = api_instance.gifs_search_get(apiKey,
                                                query, limit=25)
        lst = list(response.data)
        gif = random.choices(lst)
        await ctx.send(gif[0].url)
        return gif[0].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


async def thanks_obama(ctx):
    api_instance = giphy_client.DefaultApi()
    try:
        response = api_instance.gifs_search_get(apiKey,
                                                'thanksobama', limit=25)
        lst = list(response.data)
        gif = random.choices(lst)
        await ctx.send(gif[0].url)
        return gif[0].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

bot = commands.Bot(command_prefix='>', description="This is a Helper Bot")


async def generic_responder(message):
    api_instance = giphy_client.DefaultApi()
    query = random.choices(general)
    print(query)
    try:
        response = api_instance.gifs_search_get(apiKey,
                                                query, limit=25)
        lst = list(response.data)
        gif = random.choices(lst)
        await message.channel.send(gif[0].url)
        await bot.process_commands(message)
        return gif[0].url
    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e
