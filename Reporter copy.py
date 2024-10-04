from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot, guild_only
import discord
from better_profanity import profanity
import datetime
import asyncio
import time


BOT_TOKEN = "" #password of bot.
REPORT_CHANNEL = 1288542154670477364
GENERAL_CHANNEL = 1284558635040768022
WARN_CHANNEL = 1289535886148632638

SEVER_ID = 1284558634235465748

list = []

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot= commands.Bot(command_prefix='/',intents=intents) #init bot

profanity.load_censor_words()

badword = False

ctx = commands.Context




@bot.event
async def on_ready(): #init bot
    print('Logger Connected!')
    channel = bot.get_channel(GENERAL_CHANNEL)
    await channel.send("Logger Connected!!!")
    await bot.tree.sync()

async def warn(msg: discord.Message):
    await msg.reply(f"Please, {msg.author.name} do not send any form of bad words, Thank you!", delete_after=5)
    print(f"Please, {msg.author.name} do not send any form of bad words, Thank you!")

@bot.hybrid_command(name="warn")
async def warn_cmd(ctx: commands.Context, member: discord.Member):
    await ctx.send(f"Please, {member.name} do not send any form of bad words, Thank you!", ephemeral=True, delete_after=5)
    print(f"Please, {member.name} do not send any form of bad words, Thank you!")

@bot.hybrid_command(name="ban")
@commands.has_permissions(ban_members = True)
async def ban_cmd(ctx: commands.Context, member : discord.Member, *, reason = None):
    try: 
        await member.ban(reason = reason)
        await ctx.send(f'Banned {member.name}')
        print(f'Banned {member.name}')

    except discord.Forbidden:
        await ctx.send(f'I dont not have Permissions to do this!')
        return

@bot.hybrid_command(name="unban")
@commands.has_permissions(ban_members = True)
async def unban_cmd(ctx: commands.Context, *, member:str, reason = None):
    banned_users = await ctx.guild.bans()
    
    for ban_entry in banned_users:
        user = ban_entry.user

        if user.name == member:
            try:
                await ctx.guild.unban(user=user)
                await ctx.send(f'Unbanned {member.name}')
                print(f'Unbanned {member.name}')
            
            except discord.Forbidden:
                await ctx.send(f'I dont not have Permissions to do this!')
                return




@bot.hybrid_command(name="kick")
@commands.has_permissions(kick_members = True)
async def kick_cmd(ctx: commands.context, member: discord.Member, *, reason = None):
    try:
        await member.kick(reason = reason)
        await ctx.send(f'Kicked {member.name}')
        print(f'Kicked {member.name}')

    except discord.Forbidden:
        await ctx.send(f'I dont not have Permissions to do this!')
        return

@bot.event
async def on_message(message: discord.Message): #checking/reading the messages
    guild = bot.get_guild(SEVER_ID)
    channel2 = bot.get_channel(WARN_CHANNEL)
    
    if guild is None:
        print("No Guild")
        return
        
    channel = guild.get_channel(REPORT_CHANNEL)

    if message.author == bot.user:
        return

    anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
    too_many_vio = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member)
    bucket = anti_spam.get_bucket(message)
    retry_after = bucket.update_rate_limit()
    if retry_after:
        await message.delete()
        await message.channel.send(f"{message.author.mention}, don't spam!", delete_after=3)
        vios = too_many_vio.get_bucket(message)
        check = vios.update_rate_limit()
        if check:
            await message.author.timeout(datetime.timedelta(minutes= 10), reason="Spamming")
    

    result = profanity.contains_profanity(message.content)

    if result == True:   #deciding if they are bad and adding a report
        badword = True
        await channel.send("**Message: **" + message.content + " | " + "**User: **" + message.author.name)
        print("Message: " + message.content + " | " + "User: " + message.author.name)
        await channel.send("<@&1284787770874658939>")
        await channel2.send(f"{message.author.name} Just Got Warned!")
        with open("Logs.txt", 'a+') as fd:
            fd.seek(0)
            fd.writelines(f"Message: {message.content} | User: {message.author.name}\n")
        print(f"{message.author.name} Just Got Warned!")
        await warn(message)
        await message.delete()

        await bot.process_commands(message)

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message): #checking/reading the edited messages
    Before = before
    guild = bot.get_guild(SEVER_ID)
    channel2 = bot.get_channel(WARN_CHANNEL)
    

    if guild is None:
        print("No Guild")
        return
        
    channel = guild.get_channel(REPORT_CHANNEL)
    if after.author == bot.user:
        return

    result = profanity.contains_profanity(after.content)

    if result == True: 
        badword = True
        await channel.send("**Before Message: **" + str(before.content))
        print("Before Message: " + str(before.content))
        await channel.send("**Edited Message: **" + after.content + " | " + "**User: **" + after.author.name)
        print("Edited Message: " + after.content + " | " + "User: " + after.author.name)
        await channel.send("<@&1284787770874658939>")
        await channel2.send(f"{after.author.name} Just Got Warned!")
        with open("Logs.txt", 'a+') as fd:
            fd.seek(0)
            fd.writelines(f"Message: {before.content} | User: {before.author.name}\n")
            fd.writelines(f"Message: {after.content} | User: {after.author.name}\n")
        print(f"{after.author.name} Just Got Warned!")
        await warn(after)
        await after.delete()
        

        await bot.process_commands(after)



bot.run(BOT_TOKEN) #running the bot.
