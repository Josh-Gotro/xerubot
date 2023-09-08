import os
import random
import pyowm
import spacy


from helper_functions import youtube, giphy, thanks_obama, xeru_responder, xeru_responder_bad
from discord.ext import commands
from discord import Intents

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

intents = Intents.all()
bot = commands.Bot(command_prefix='>', description="This is a Helper Bot", intents=intents)

nlp = spacy.load("en_core_web_sm")
api_key = os.environ.get('OWM_API_KEY')
owm = pyowm.OWM(api_key)
mgr = owm.weather_manager()


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
    if "noxeru" in message.content.lower():
        # await bot.wait_until_ready()
        await xeru_responder_bad(message, bot)

    if "okcourser" in message.content.lower():
        ctx = await bot.get_context(message)
        await giphy(ctx, "calculator")
        return gif[0].url

    if "weather" in message.content.lower():
        doc = nlp(message.content)
        location = None

        for ent in doc.ents:
            if ent.label_ == "GPE":
                location = ent.text
            elif ent.text == "juneau,":
                location = "Juneau, US"

        if location:
            observation = mgr.weather_at_place(str(location))
            w = observation.weather
            temperature = w.temperature('fahrenheit')['temp']
            maxtemp = w.temperature('fahrenheit')['temp_max']
            mintemp = w.temperature('fahrenheit')['temp_min']
            await message.channel.send(f"The current temp in {location} is {temperature}°F.")
            await message.channel.send(f"High forecast today: {maxtemp}°F")
            await message.channel.send(f"Low forecast today:  {mintemp}°F")
            return
        return

    if message.author == bot.user:
        return

#  5% chance to respond when courser talks with a calulator gif
    specific_user_id = 176061042101583872
    if message.author.id == specific_user_id:
        roulette = random.randint(1, 100)
        if roulette <= 5:  # 5% chance
            ctx = await bot.get_context(message)
            await giphy(ctx, "calculator")

bot.run(token)
