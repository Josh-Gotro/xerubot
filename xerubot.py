import discord
import datetime
import random
import os
import urllib.parse
import urllib.request
import re
import giphy_client

from giphy_client.rest import ApiException
from discord.ext import commands
from discord.utils import get
from data import general

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

bot = commands.Bot(command_prefix='>', description="This is a Helper Bot")

# -------> Events


@bot.event
async def on_ready():
    print(f'{bot.user.name} connected\n')


# -------> Commands
#  >ping
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

#  >sum 1 2


@bot.command()
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne + numTwo)

    #  >inflation


@bot.command()
async def inflation(ctx):
    api_instance = giphy_client.DefaultApi()
    randOffset = random.randint(1, 80)
    try:
        response = api_instance.gifs_search_get(apiKey,
                                                'thanksobama', limit=25)
        lst = list(response.data)
        gif = random.choices(lst)
        await ctx.send(gif[0].url)
        return gif[0].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

#  >info


@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Lorem Ipsum asdasd",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(
        url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

    await ctx.send(embed=embed)

#  >yt tinycakes


@bot.command()
async def yt(ctx, *, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})',
                                htm_content.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

# >gif UwU


@bot.command()
async def gif(ctx, query):
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


@bot.command()
async def okxeru(ctx):
    api_instance = giphy_client.DefaultApi()
    query = random.choices(general)
    print(query)
    try:
        response = api_instance.gifs_search_get(apiKey,
                                                query, limit=25)
        lst = list(response.data)
        gif = random.choices(lst)
        await ctx.send(gif[0].url)
        return gif[0].url
    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

# -------> Listen

# @bot.listen()
# async def on_message(message):
#     if "tutorial" in message.content.lower():
#         # in this case don't respond with the word "Tutorial" or you will call the on_message event recursively
#         await message.channel.send('This is that you want http://youtube.com/fazttech')
#         await bot.process_commands(message)

bot.run(token)
