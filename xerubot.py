import discord
import datetime
import random
import os
import giphy_client

from helper_functions import youtube, giphy, thanks_obama
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
@bot.command()
#  >ping
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
#  >sum 1 2
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne + numTwo)


@bot.command()
#  >inflation
async def inflation(ctx):
    await thanks_obama(ctx)


@bot.command()
#  >info
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Lorem Ipsum asdasd",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Members", value=f"{ctx.guild.members}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(
        url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

    await ctx.send(embed=embed)


@bot.command()
#  >yt tinycakes
async def yt(ctx, *, search):
    await youtube(ctx, search)


@bot.command()
# >gif UwU
async def gif(ctx, query):
    await giphy(ctx, query)


#  -------> Listen
@bot.listen()
async def on_message(message):
    if "okxeru" in message.content.lower():
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
bot.run(token)
