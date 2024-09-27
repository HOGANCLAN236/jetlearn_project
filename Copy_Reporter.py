from discord import app_commands
import os
from discord.ext import commands
import discord
import aiofiles
from better_profanity import profanity

BOT_TOKEN = "" #password of bot.
REPORT_CHANNEL = 1288542154670477364
GENERAL_CHANNEL = 1284558635040768022

SEVER_ID = 1284558634235465748

list = []

intents = discord.Intents.all()
intents.message_content = True
bot= commands.Bot(command_prefix='!',intents=intents) #init bot

profanity.load_censor_words()
result = profanity.contains_profanity("")


@bot.event
async def on_ready(): #init bot
    print('Logger Connected!')
    channel = bot.get_channel(GENERAL_CHANNEL)
    await channel.send("Logger Connected!!!")

@bot.event
async def on_message(message): #chacking/reading the messages
    guild = bot.get_guild(SEVER_ID)
    

    if guild is None:
        print("No Guild")
        return
        
    channel = guild.get_channel(REPORT_CHANNEL)

    if message.author == bot.user:
        return

    for i in list:   #deciding if they are bad and adding a report
        if message.content.startswith(i):
            await channel.send("**Message: **" + i + " | " + "**User: **" + message.author.name)
            await channel.send("<@&1284787770874658939>")


@bot.event
async def on_message_edit(before, after): #checking/reading the edited messages
    Before = before
    guild = bot.get_guild(SEVER_ID)
    

    if guild is None:
        print("No Guild")
        return
        
    channel = guild.get_channel(REPORT_CHANNEL)
    if after.author == bot.user:
        return

    for i in list:   #deciding if they are bad and adding a report
        if after.content.startswith(i):
            await channel.send("**Before Message: **" + str(Before))
            await channel.send("**Edited Message: **" + i + " | " + "**User: **" + after.author.name)
            await channel.send("<@&1284787770874658939>")


bot.run(BOT_TOKEN) #running the bot.
