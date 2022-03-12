import os
import random

from helper_functions import youtube, giphy, thanks_obama, xeru_responder, xeru_responder_bad
from discord.ext import commands
# from discord.utils import get

if not os.environ.get('TOKEN'):
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv('TOKEN')
    apiKey = os.getenv("API_KEY")
    # myID = os.getenv("MY_DISCORD_ID")
else:
    token = os.environ.get('TOKEN')
    apiKey = os.environ.get("API_KEY")
    # myID = os.environ.get("MY_DISCORD_ID")

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
        # await bot.wait_until_ready()
        await xeru_responder(message, bot)
    if "gatorade me" in message.content.lower():
        ctx = await bot.get_context(message)
        await giphy(ctx, "gatorade+me")
    if "i love" in message.content.lower():
        ctx = await bot.get_context(message)
        roulette = random.randint(1, 10)
        if roulette == 5:
            await message.channel.send("if you love it so much then...")
            await giphy(ctx, "wedding")
    if "i like" in message.content.lower():
        ctx = await bot.get_context(message)
        roulette = random.randint(1, 10)
        if roulette == 5:
            await message.channel.send("if you like it so much then...")
            await giphy(ctx, "wedding")
        return gif[0].url
    if "badxeru" in message.content.lower():
        # await bot.wait_until_ready()
        await xeru_responder_bad(message, bot)

bot.run(token)
