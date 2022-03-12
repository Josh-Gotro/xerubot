import os

from helper_functions import youtube, giphy, thanks_obama, generic_responder
from discord.ext import commands

if not os.environ.get('TOKEN'):
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv('TOKEN')
else:
    token = os.environ.get('TOKEN')

bot = commands.Bot(command_prefix='>', description="This is a Helper Bot")

#  -------> Events


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
        generic_responder(message)
bot.run(token)
