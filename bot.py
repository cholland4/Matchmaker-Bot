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
async def on_guild_join(guild):
    add_server(guild.id, str(guild.name))


@client.event
async def on_guild_remove(guild):
    remove_server(guild.id)


@client.event
async def on_message(message):
    # add_server(message.guild.id, str(message.guild.name))
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
    for server in client.guilds:
        clear_queue(server.id, server.name)
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


@client.command()
async def commands(ctx):
    ''' Prints working commands.
        '''
    message = """To input your SR, please use the following commands:
        .tank 1000-5000
        .dps 1000-5000
        .support 1000-5000
        \nTo see your SR, use .sr
        \nTo queue for a role, use .q role
To leave the queue, use .q leave or .leave or .l
To see the current queue, use .q
        \nTo see what you are queued for, use .status
        \nTo see the roles needed to make a match, use .roles
        \nTo begin matchmaking, use .mm
        \nTo report the winning team, use .win 1/2
        \nIn case of a tie, use .win 0"""
    """
        \nTo move users to team channels after matchmaking, use .mtt
        \nTo move users from team channels back to draft, use .mtd
        """
    await ctx.send("```" + message + "```")
    try:
        await ctx.message.delete()
    except:
        pass


@client.command(aliases=["matchmake"])
async def mm(ctx):
    ''' Makes a match based on users queued. If not enough players
                are queued prints an error message.
        '''
    server_id = ctx.message.guild.id
    server_name = str(ctx.message.guild.name)
    user_data = load_user_data()
    match_list = matchmake(user_data)
    if match_list[0] != -1:
        # await ctx.send(printTeams(matchList))
        # savePlayerData(matchList[0])
        await ctx.send(randomMap())
    else:
        await ctx.send("Error encountered. Are enough players queued?",
                       delete_after=30)
    try:
        await ctx.message.delete()
    except:
        pass


@client.command(aliases=["randomMap", "randommap"])
async def map(ctx):
    ''' Sends a random map.
        '''
    await ctx.send(randomMap())
    try:
        await ctx.message.delete()
    except:
        pass


@client.command(aliases=["btag", "tag"])
async def battletag(ctx, btag):
    discord_id = ctx.message.author.id
    discord_name = str(ctx.message.author)
    if set_battletag(discord_id, discord_name, btag):
        await ctx.send(ctx.message.author.mention +
                       ", " + btag +
                       " has been saved as your battletag. " +
                       "Use .update to pull data from Overwatch " +
                       "after ensuring your profile is public."
                       , delete_after=25)
    else:
        await ctx.send(ctx.message.author.mention +
                       ", something went wrong.", delete_after=15)
    try:
        await ctx.message.delete()
    except:
        pass



@client.command(aliases=["supp"])
async def support(ctx, sr):
    ''' Updates the sender's profile with the new support data.
    '''
    try:
        sr = int(sr)
    except ValueError:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.",
                       delete_after=25)
        return
    discord_id = ctx.message.author.id
    discord_name = str(ctx.message.author)
    print(discord_name)
    get_user_by_id(discord_id, discord_name)
    if set_support_sr(discord_id, discord_name, sr):
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
async def damage(ctx, sr):
    ''' Updates the sender's profile with the new support data.
    '''
    try:
        sr = int(sr)
    except ValueError:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.",
                       delete_after=25)
        return
    discord_id = ctx.message.author.id
    discord_name = str(ctx.message.author)
    print(discord_name)
    get_user_by_id(discord_id, discord_name)
    if set_dps_sr(discord_id, discord_name, int(sr)):
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
async def tank(ctx, sr):
    ''' Updates the sender's profile with the new support data.
    '''
    try:
        sr = int(sr)
    except ValueError:
        await ctx.send(ctx.message.author.mention +
                       ", please enter a valid integer.",
                       delete_after=25)
        return
    discord_id = ctx.message.author.id
    discord_name = str(ctx.message.author)
    print(discord_name)
    get_user_by_id(discord_id, discord_name)
    if set_tank_sr(discord_id, discord_name, int(sr)):
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


@client.command(aliases=["q"])
async def queue(ctx, role=None):
    ''' If no args passed, prints the queue. Else it updates the
                sender's data to place them in the queue for what role
                they want.
        '''
    discord_id = ctx.message.author.id
    discord_name = str(ctx.message.author)
    server_id = ctx.message.guild.id
    server_name = str(ctx.message.guild.name)
    if role is None:
        await ctx.send(ctx.message.author.mention
                       + "\n" + printQueue(server_id, server_name),
                       delete_after=15)
    elif role == "clear":
        clear_queue(server_id, server_name)
        await ctx.send("The queue has been emptied.",
                       delete_after=25)
    elif role == "fill":
        queued = num_queued(server_id, server_name)
        roles_needed = []
        if queued[0] < 4:
            roles_needed.append("tank")
        if queued[1] < 4:
            roles_needed.append("dps")
        if queued[2] < 4:
            roles_needed.append("support")
        if len(roles_needed) == 0:
            roles_needed = ["tank", "dps", "support"]

        rand = random.randint(0, len(roles_needed) - 1)
        message = (queueFor(discord_id, discord_name, server_id, server_name, roles_needed[rand]))
        await ctx.send(ctx.message.author.mention + ", " +
                       message, delete_after=15)
        await roles(ctx, 10)
    elif role == "leave":
        await leave(ctx)
    else:
        message = (queueFor(discord_id, discord_name, server_id, server_name, role))
        await ctx.send(ctx.message.author.mention + ", " +
                       message, delete_after=25)
        await roles(ctx, 10)
    try:
        await ctx.message.delete()
    except:
        pass


@client.command(aliases=["role"])
async def roles(ctx, timer=25):
    ''' Prints out the roles needed to matchmake.
        '''
    server_id = ctx.message.guild.id
    server_name = str(ctx.message.guild.name)
    message = "Roles Needed:\n"
    queued = num_queued(server_id, server_name)
    if 4 - queued[0] > 0:
        message = message + str(4 - queued[0]) + " tanks.\n"
    if 4 - queued[1] > 0:
        message = message + str(4 - queued[1]) + " dps.\n"
    if 4 - queued[2] > 0:
        message = message + str(4 - queued[2]) + " supports.\n"
    if message == "Roles Needed:\n":
        message = "All roles filled."
    await ctx.send(message, delete_after=timer)
    try:
        await ctx.message.delete()
    except:
        pass


@client.command(aliases=["l"])
async def leave(ctx):
    ''' Leaves the queue.
        '''
    discord_id = ctx.message.author.id
    discord_name = str(ctx.message.author)
    server_id = ctx.message.guild.id
    server_name = str(ctx.message.guild.name)
    message = deQueue(discord_id, discord_name, server_id, server_name)
    await ctx.send(ctx.message.author.mention + ", " +
                   message, delete_after=15)
    await roles(ctx, 10)
    try:
        await ctx.message.delete()
    except:
        pass


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
