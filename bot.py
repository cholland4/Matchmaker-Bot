import discord
import random
from discord.ext import commands
from bot_data_functions import *
from bot_matchmake_functions import *
from discord import ChannelType
import asyncio
from discord.utils import get
# import datetime

client = commands.Bot(command_prefix=".")

global bot_owner


@client.event
async def on_message(message):
    
    await client.process_commands(message)


# @client.event
# async def on_member_remove(guild, user):
#        delete_player(str(user.id))


@client.event
async def on_ready():
    ''' Prints a message when the bot is ready.
        '''
    global bot_owner
    bot_owner = client.get_user(176510548702134273)
    print("bot is ready")


@client.command()
async def bug(ctx, *issue):
    global bot_owner
    guild_id = str(ctx.message.guild.id)
    guild_name = str(ctx.message.guild.name)
    sender = str(ctx.message.author)

    message = ("Ah, shit. Bug report from " + sender +
               "\nServer Name: " + guild_name +
               "\nServer ID: " + guild_id +
               "\nIssue: ")
    for word in issue:
        message = message + word + " "

    await bot_owner.send(message)
    await ctx.send("Your bug report has been ~~ignored~~ received.")
    try:
        await ctx.message.delete()
    except:
        pass


@client.command(aliases=["supp"])
async def support(ctx, SR):
    ''' Updates the sender's profile with the new support data.
    '''
    try:
        SR = int(SR)
    except ValueError:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.",
                       delete_after=25)
        return
    discord_id = ctx.message.author.id
    discord_name = str(ctx.message.author)
    print(discord_name)
    get_user_by_id(discord_id, discord_name)
    if set_support_sr(discord_id, discord_name, SR):
        await ctx.send(ctx.message.author.mention +
                       ", your support SR has been updated.",
                       delete_after=25)
    else:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.",
                       delete_after=25)
    try:
        await ctx.message.delete()
    except:
        pass
    # await ctx.send(print_user(discord_id))


@client.command(aliases=["dps"])
async def damage(ctx, SR):
    ''' Updates the sender's profile with the new support data.
    '''
    try:
        SR = int(SR)
    except ValueError:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.",
                       delete_after=25)
        return
    discord_id = ctx.message.author.id
    discord_name = str(ctx.message.author)
    print(discord_name)
    get_user_by_id(discord_id, discord_name)
    if set_dps_sr(discord_id, discord_name, int(SR)):
        await ctx.send(ctx.message.author.mention +
                       ", your dps SR has been updated.",
                       delete_after=25)
    else:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.",
                       delete_after=25)
    try:
        await ctx.message.delete()
    except:
        pass
    # await ctx.send(print_user(discord_id))


@client.command()
async def tank(ctx, SR):
    ''' Updates the sender's profile with the new support data.
    '''
    try:
        SR = int(SR)
    except ValueError:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.",
                       delete_after=25)
        return
    discord_id = ctx.message.author.id
    discord_name = str(ctx.message.author)
    print(discord_name)
    get_user_by_id(discord_id, discord_name)
    if set_tank_sr(discord_id, discord_name, int(SR)):
        await ctx.send(ctx.message.author.mention +
                       ", your tank SR has been updated.",
                       delete_after=25)
    else:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.",
                       delete_after=25)
    try:
        await ctx.message.delete()
    except:
        pass
    # await ctx.send(print_user(discord_id))


@client.command()
async def sr(ctx):
    discord_id = ctx.message.author.id
    discord_name = str(ctx.message.author)
    await ctx.send(print_user(discord_id, discord_name))


@client.command(aliases=["flip"])
async def coin(ctx):
    ''' Flips a coin.
        '''
    result = random.randint(0, 1)
    if result == 0:
        await ctx.send("Heads!")
    else:
        await ctx.send("Tails!")
    try:
        await ctx.message.delete()
    except:
        pass


@client.command()
async def clear(ctx, amount=5):
    ''' Removes a specified amount of messages.
        '''
    if str(ctx.message.author.id) == "176510548702134273":
        if amount > 0:
            await ctx.channel.purge(limit=amount + 1)


tokenfile = open("token.txt", "r")
token = tokenfile.readline()
tokenfile.close()
client.run(token)
