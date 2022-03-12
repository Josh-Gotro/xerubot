import urllib.parse
import urllib.request
import re
import random
import giphy_client
import os

from giphy_client.rest import ApiException
from data import general, bad
from discord.ext import commands

if not os.environ.get('TOKEN'):
    from dotenv import load_dotenv
    load_dotenv()
    apiKey = os.getenv("API_KEY")
else:
    apiKey = os.environ.get("API_KEY")


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


async def xeru_responder(message, bot):
    api_instance = giphy_client.DefaultApi()
    query = random.choices(general)
    print(query)
    try:
        response = api_instance.gifs_search_get(apiKey,
                                                query, limit=20)
        lst = list(response.data)
        gif = random.choices(lst)
        await message.channel.send(gif[0].url)
        await bot.process_commands(message)
        return gif[0].url
    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n\n\n" % e


async def xeru_responder_bad(message, bot):
    api_instance = giphy_client.DefaultApi()
    query = random.choices(bad)
    print(query)
    try:
        response = api_instance.gifs_search_get(apiKey,
                                                query, limit=20)
        lst = list(response.data)
        gif = random.choices(lst)
        await message.channel.send(gif[0].url)
        await bot.process_commands(message)
        return gif[0].url
    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n\n\n" % e
