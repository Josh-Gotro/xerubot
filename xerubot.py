import os
import random
import pyowm
import spacy
import logging


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

intents = Intents.default()
bot = commands.Bot(command_prefix='>', description="This is a Helper Bot", intents=intents)


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


nlp = spacy.load("en_core_web_sm")
api_key = os.environ.get('OWM_API_KEY')
owm = pyowm.OWM(api_key)



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

    logging.info(f"Message received: {message.content}")  # Debug line

    if "weather" in message.content.lower():
        logging.info("Found 'weather' in the message.")  # Debug line
        doc = nlp(message.content)
        for ent in doc.ents:
            logging.info(f"Entity found: {ent.text}, Label: {ent.label_}")  # Debug line
            if ent.label_ == "GPE":
                location = ent.text
                logging.info(f"Fetching weather for {location}.")  # Debug line
                observation = owm.weather_at_place(location)
                w = observation.get_weather()
                temperature = w.get_temperature('fahrenheit')["temp"]
                await message.channel.send(f"The current temperature in {location} is {temperature}°F.")
                return
        logging.info("No location found in message.")  # Debug line

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
