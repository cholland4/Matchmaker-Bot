import discord
import random
from discord.ext import commands
from bot_data_functions import *
from bot_matchmake_functions import *
from discord import ChannelType
import asyncio
from discord.utils import get
import datetime

client = commands.Bot(command_prefix = ".")

global bot_owner

@client.event
async def on_guild_join(guild):
	create_guild(str(guild.id))

##@client.command()
##async def passive_aggressive_sarcasm(ctx):
##        await ctx.send("Gee Duncan, thanks for all the help with testing the bot." +
##                       " I'm sure without you I couldn't have tried those two commands on my own." +
##                       "Thanks for all the help from the bottom of my heart.")
	
	
@client.event
async def on_guild_remove(guild):
	delete_guild(str(guild.id))


##@client.event
##async def on_member_remove(guild, user):
##        delete_player(str(user.id))

	
@client.event
async def on_ready():

        ''' Prints a message when the bot is ready.
        '''
        global bot_owner
        bot_owner = client.get_user(176510548702134273)
        for guild in client.guilds:
                ##create_guild(str(guild.id))
                clearQueue(str(guild.id))
        loadAllData()
        await client.change_presence(activity=discord.Game(name=".help"))
        print("bot is ready")


##@client.command()
##async def createServerData(ctx):
##        guild_id = str(ctx.message.guild.id)
##        if str(ctx.message.author.id) == "176510548702134273":
##                create_guild(guild_id)
##                await ctx.send("Server template set up.",delete_after=5)
##        try:
##                await ctx.message.delete()
##        except:
##                pass
                

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
async def vip(ctx, action):
        guild_id = str(ctx.message.guild.id)
        if str(ctx.message.author.id) == "176510548702134273":
                if action == "add":
                        for user in ctx.message.mentions:
                                addVip(guild_id, str(user.id))
                        await ctx.send("VIP status granted.") #,delete_after=5)
                elif action == "remove" or action == "revoke":
                        for user in ctx.message.mentions:
                                removeVip(guild_id, str(user.id))
                        await ctx.send("VIP status revoked.") #,delete_after=5)
        else:
                await ctx.send("You do not have permission to add VIPs!",
                               delete_after=5)
##        try:
##                await ctx.message.delete()
##        except:
##                pass


@client.command(aliases=["btag", "tag"])
async def battletag(ctx, btag):
        guild_id = str(ctx.message.guild.id)
        if setBtag(btag, str(ctx.message.author.id), guild_id):
                await ctx.send(ctx.message.author.mention +
                               ", " + btag +
                               " has been saved as your battletag. " +
                               "Use .update to pull data from Overwatch " +
                               "after ensuring your profile is public."
                               ,delete_after=25)
        else:
                await ctx.send(ctx.message.author.mention +
                               ", something went wrong.",delete_after=15)
        try:
                await ctx.message.delete()
        except:
                pass


@client.command()
async def update(ctx):
        ''' Updates the player data based off their in game profile.
        '''
        guild_id = str(ctx.message.guild.id)
        await ctx.send("This may take a while and will pause all " +
                       "other commands. Please be patient and do not spam it.",
                       delete_after=25)
        
        if pullSR(str(ctx.message.author.id), str(ctx.message.author), guild_id):
                await ctx.send(ctx.message.author.mention +
                               ", success! Your data has been imported." +
                               " If you are not placed or not public, data" +
                               " will not be overwritten."
                               ,delete_after=25)
        else:
                await ctx.send(ctx.message.author.mention +
                               ", something went wrong. Is your profile " +
                               "public and have you completed any placements?"
                               ,delete_after=25)
        try:
                await ctx.message.delete()
        except:
                pass

        
##@client.command(aliases=["pugs"])
##async def schedule(ctx, time, metric):
##        ''' Schedules a pug event some time in the future.
##        '''
##        if str(ctx.message.author.id) in vip_list:
##                # await ctx.message.delete()
##                now = datetime.datetime.now()
##                sleep_timer = 0
##                
##                if metric.lower() == "s":
##                        sleep_timer = int(time)
##                elif metric.lower() == "m":
##                        sleep_timer = int(time) * 60
##                elif metric.lower() == "h":
##                        sleep_timer = int(time) * 60 * 60
##                
##                for i in ctx.message.guild.roles:
##                        if str(i) == "Puggers":
##                                role = i
##                try:
##                        poll = await ctx.send(role.mention +
##                                              ", react if you're down " +
##                                              "for pugs in " + time + metric)
##                except:
##                        poll = await ctx.send("React if you're down for pugs in "
##                                              + time + metric)
##                   
##                check = '✅'
##                rart = 'Rart:658615209463775242'
##                await poll.add_reaction(rart)
##                  
##                await asyncio.sleep(sleep_timer)
##
##                try:
##                        cache_poll = await ctx.fetch_message(poll.id)
##                        
##                        num_puggers = 0
##                        for reaction in cache_poll.reactions:
##                                print(str(reaction))
##                                if str(reaction) == "<:Rart:658615209463775242>":
##                                        num_puggers = reaction.count - 1
##
##                        if num_puggers > 12:
##                                try:
##                                        await ctx.send(role.mention +
##                                               " the time for pugs is upon us!")
##                                except:
##                                        await ctx.send("It's pugs time!")
##                        else:
##                                await ctx.send("Not enough people responded." +
##                                               " Please get " +
##                                               str(12-num_puggers) + " more.")
##                except:
##                        await ctx.send("A scheduling error occured. "
##                                       "Was the original message deleted?")
##        try:
##                await ctx.message.delete()
##        except:
##                pass

        
##@client.event
##async def on_message(message):
##    channel = message.channel
##    mystr = message.content
##    sender = str(message.author)
##    await client.process_commands(message)


@client.command()
async def shock(ctx):
        ''' Shock
        '''
        await ctx.send("Shock did it without sinatraa fuck all " +
                       "yall that doubted and said super is a " +
                       "benched player. Thank you for reading my " +
                       "PSA have a good night see you guys for pugs")
        try:
                await ctx.message.delete()
        except:
                pass


@client.command(aliases=["setD"])
async def setChannelDraft(ctx, channel_id):
        ''' Enter the channel id of the draft channel.
        '''
        try:
                await ctx.message.delete()
        except:
                pass
        guild_id = str(ctx.message.guild.id)
        setChannelID(guild_id, "draft_channel", channel_id)


@client.command(aliases=["setT1"])
async def setChannel1(ctx, channel_id):
        ''' Enter the channel id of the team 1 channel.
        '''
        try:
                await ctx.message.delete()
        except:
                pass
        guild_id = str(ctx.message.guild.id)
        setChannelID(guild_id, "t1_channel", channel_id)


@client.command(aliases=["setT2"])
async def setChannel2(ctx, channel_id):
        ''' Enter the channel id of the team 2 channel.
        '''
        try:
                await ctx.message.delete()
        except:
                pass
        guild_id = str(ctx.message.guild.id)
        setChannelID(guild_id, "t2_channel", channel_id)


@client.command(aliases=["mtt"])
#@commands.has_role('BotMaster')
async def move_to_teams(ctx):
        ''' Moves people on teams to their respective team channel.
        '''
        try:
                await ctx.message.delete()
        except:
                pass
        guild_id = str(ctx.message.guild.id)
        vip_list = getVipList(guild_id)
        if str(ctx.message.author.id) in vip_list:
                """
                ## ## MatchMaking Bot Testing channel IDs
                if ctx.message.guild.id == 651200164169777154:
                        draft_channel = client.get_channel(709248862828888074)
                        channel1 = client.get_channel(707749575108198441)
                        channel2 = client.get_channel(707749630728732712)

                ## ## We Use this channel IDs
                if ctx.message.guild.id == 442813167148728330:
                        draft_channel = client.get_channel(652717496045928458)
                        channel1 = client.get_channel(647667378334990377)
                        channel2 = client.get_channel(647667443782909955)
                """
                draft_channel = client.get_channel(getChannelID(guild_id,
                                                                "draft_channel"))
                channel1 = client.get_channel(getChannelID(guild_id,
                                                           "t1_channel"))
                channel2 = client.get_channel(getChannelID(guild_id,
                                                           "t2_channel"))
                
                pdata = loadPlayerData(guild_id)
                team1 = get_team_id(pdata, 1, guild_id)
                team2 = get_team_id(pdata, 2, guild_id)
                # sender = ctx.message.author
                num_moved = 0
                for member in ctx.message.guild.members:
                        if member.id in team1:
                                if member in draft_channel.members:
                                        # await member.move_to(channel1)
                                        await member.edit(voice_channel=channel1)
                                        num_moved += 1
                        elif member.id in team2:
                                if member in draft_channel.members:
                                        # await member.move_to(channel2)
                                        await member.edit(voice_channel=channel2)
                                        num_moved += 1
                await ctx.send("{} users moved.".format(num_moved),
                               delete_after=3)


@client.command(aliases=["mtd"])
#@commands.has_role('BotMaster')
async def move_to_draft(ctx):
        ''' Moves all users from the team channels to the draft channel.
        '''
        try:
                await ctx.message.delete()
        except:
                pass
        guild_id = str(ctx.message.guild.id)
        vip_list = getVipList(guild_id)
        if str(ctx.message.author.id) in vip_list:
                """
                ## ## MatchMaking Bot Testing channel IDs
                if ctx.message.guild.id == 651200164169777154:
                        draft_channel = client.get_channel(709248862828888074)
                        channel1 = client.get_channel(707749575108198441)
                        channel2 = client.get_channel(707749630728732712)

                ## ## We Use this channel IDs
                if ctx.message.guild.id == 442813167148728330:
                        draft_channel = client.get_channel(652717496045928458)
                        channel1 = client.get_channel(647667378334990377)
                        channel2 = client.get_channel(647667443782909955)
                """
                draft_channel = client.get_channel(getChannelID(guild_id,
                                                                "draft_channel"))
                channel1 = client.get_channel(getChannelID(guild_id,
                                                           "t1_channel"))
                channel2 = client.get_channel(getChannelID(guild_id,
                                                           "t2_channel"))
                num_moved = 0
                for member in channel1.members:
##                        await member.move_to(draft_channel)
                        await member.edit(voice_channel=draft_channel)
                        num_moved += 1
                for member in channel2.members:
##                        await member.move_to(draft_channel)
                        await member.edit(voice_channel=draft_channel)
                        num_moved += 1
                await ctx.send("{} users moved.".format(num_moved),
                               delete_after=3)


@client.command()
async def captains(ctx):
        ''' Picks two users at random from draft channel.
        '''        
        guild_id = str(ctx.message.guild.id)
        draft_channel = client.get_channel(getChannelID(guild_id, "draft_channel"))

        if len(draft_channel.members) < 2:
                await ctx.send("Not enough players in the draft channel!",
                               delete_after=15)
        else:
                i = random.randint(0, len(draft_channel.members)-1)
                j = random.randint(0, len(draft_channel.members)-1)
                while i == j:
                        j = random.randint(0, len(draft_channel.members))
                await ctx.send(draft_channel.members[i].mention + " " +
                               draft_channel.members[j].mention +
                               " are your captains.")
        try:
                await ctx.message.delete()
        except:
                pass


@client.command()
async def team(ctx):
        ''' Reminds the sender what team they're on.
        '''
        try:
                await ctx.message.delete()
        except:
                pass
        sender = str(ctx.message.author.id)
        guild_id = str(ctx.message.guild.id)
        team = getPlayerTeam(sender, guild_id)
        if team == "-1":
                await ctx.send(ctx.message.author.mention +
                               ", you're not on a team."
                               ,delete_after=15)
        else:
                await ctx.send(ctx.message.author.mention +
                               ", you're on team " + str(team),
                               delete_after=15)
        try:
                await ctx.message.delete()
        except:
                pass


@client.command(aliases=["randomMap", "randommap"])
async def map(ctx):
        ''' Sends a random map.
        '''
        if str(ctx.message.author) == "TheGlare#1451":
                # await ctx.message.delete()
                await ctx.send("King's Row")
        else:
                await ctx.send(randomMap())
                
        try:
                await ctx.message.delete()
        except:
                pass


@client.command()
async def mention(ctx):
        ''' Mentions whoever used the command.
        '''
        sleep_timer = random.randint(1, 120)
        print(sleep_timer)
        await asyncio.sleep(sleep_timer)
        await ctx.send(ctx.message.author.mention,delete_after=30)
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
        guild_id = str(ctx.message.guild.id)
        mylist = getAllPlayerData(guild_id)
        matchList = matchmake(mylist)
        if matchList[0] != -1:
                await ctx.send(printTeams(matchList))
                savePlayerData(matchList[0])
                await ctx.send(randomMap())
                setGameStatus(guild_id, True)
        else:
                await ctx.send("Error encountered. Are enough players queued?",
                               delete_after=30)
        try:
                await ctx.message.delete()
        except:
                pass
        

@client.command(aliases=["w"])
async def win(ctx, team_num):
        ''' Calls adjust to add or subtract player SR.
        '''
        guild_id = str(ctx.message.guild.id)
        if (team_num == "0" or team_num == "1" or team_num == "2") \
           and gameStatus(guild_id):
                adjust(int(team_num))
                if team_num != "0":
                        await ctx.send("Congrats Team " +
                                       team_num)
                else:
                        await ctx.send("My algorithm is so good, " +
                                       "the teams were perfectly balanced.")
                clearQueue()
                await client.change_presence(activity=discord.Game(name=""))
                setGameStatus(guild_id, False)
        else:
                if(gameStatus(guild_id)):
                        await ctx.send("Please enter a valid team.")
                else:
                      await ctx.send("No game in progress.")
        try:
                await ctx.message.delete()
        except:
                pass


@client.command(aliases=["supp"])
async def support(ctx, SR):
        ''' Updates the sender's profile with the new support data.
        '''
        sender = str(ctx.message.author)
        discord_id = str(ctx.message.author.id)
        guild_id = str(ctx.message.guild.id)
        if setSupport(SR, discord_id, sender, guild_id):
                await ctx.send(ctx.message.author.mention +
                               ", your support SR has been updated.",
                               delete_after=25)
        elif int(SR) <= 1000:
                await ctx.send(ctx.message.author.mention +
                               ", please rank up and try again.",
                               delete_after=25)
        else:
                await ctx.send(ctx.message.author.mention +
                               ", please enter a valid integer.",
                               delete_after=25)
        try:
                await ctx.message.delete()
        except:
                pass

@client.command(aliases=["dps"])
async def damage(ctx, SR):
        ''' Updates the sender's profile with the new dps data.
        '''
        sender = str(ctx.message.author)
        discord_id = str(ctx.message.author.id)
        guild_id = str(ctx.message.guild.id)
        if setDamage(SR, discord_id, sender, guild_id):
                await ctx.send(ctx.message.author.mention +
                               ", your dps SR has been updated.",
                               delete_after=25)
        elif int(SR) <= 1000:
                await ctx.send(ctx.message.author.mention +
                               ", please rank up and try again.",
                               delete_after=25)
        else:
                await ctx.send(ctx.message.author.mention +
                               ", please enter a valid integer.",
                               delete_after=25)
        try:
                await ctx.message.delete()
        except:
                pass

@client.command()
async def tank(ctx, SR):
        ''' Updates the sender's profile with the new tank data.
        '''
        sender = str(ctx.message.author)
        discord_id = str(ctx.message.author.id)
        guild_id = str(ctx.message.guild.id)
        if setTank(SR, discord_id, sender, guild_id):
                await ctx.send(ctx.message.author.mention +
                               ", your tank SR has been updated.",
                               delete_after=25)
        elif int(SR) <= 1000:
                await ctx.send(ctx.message.author.mention +
                               ", please rank up and try again.",
                               delete_after=25)
        else:
                await ctx.send(ctx.message.author.mention +
                               ", please enter a valid integer.",
                               delete_after=25)
        try:
                await ctx.message.delete()
        except:
                pass


@client.command(aliases=["q"])
async def queue(ctx, role="none"):
        ''' If no args passed, prints the queue. Else it updates the
                sender's data to place them in the queue for what role
                they want.
        '''
        guild_id = str(ctx.message.guild.id)
        if gameStatus(guild_id):
                await ctx.send("Please report a winner before queuing!",
                               delete_after=25)
        else:
                if role == "none":
                        await ctx.send(ctx.message.author.mention
                                       + "\n" + printQueue(guild_id),
                                       delete_after=15)
                elif role == "clear":
                        clearQueue(guild_id)
                        await ctx.send("The queue has been emptied.",
                               delete_after=25)
                elif role == "fill":
                        roles_needed = []
                        if suppQueued(guild_id) != 0:
                                roles_needed.append("support")
                        if tankQueued(guild_id) != 0:
                                roles_needed.append("tank")
                        if dpsQueued(guild_id) != 0:
                                roles_needed.append("dps")
                        if len(roles_needed) == 0:
                                roles_needed = ["tank", "support", "dps"]
                        
                        rand = random.randint(0, len(roles_needed)-1)
                        sender = str(ctx.message.author.id)
                        message = (queueFor(roles_needed[rand], sender, guild_id))
                        await ctx.send(ctx.message.author.mention + ", " +
                                       message, delete_after=15)
                        await roles(ctx, 10)
                elif role == "leave":
                        await leave(ctx)
                else:
                        sender = str(ctx.message.author.id)
                        message = (queueFor(role, sender, guild_id))
                        await ctx.send(ctx.message.author.mention + ", " +
                                       message,delete_after=25)
                        await roles(ctx, 10)
        try:
                await ctx.message.delete()
        except:
                pass


@client.command(aliases=["role"])
async def roles(ctx, timer=25):
        ''' Prints out the roles needed to matchmake.
        '''
        guild_id = str(ctx.message.guild.id)
        message = "Roles Needed:\n"
        if tankQueued(guild_id) != 0:
                message = message + (tankQueued(guild_id) + " tanks.\n")
        if dpsQueued(guild_id) != 0:
                message = message + (dpsQueued(guild_id) + " dps.\n")
        if suppQueued(guild_id) != 0:
                message = message + (suppQueued(guild_id) + " supports.\n")
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
        sender = str(ctx.message.author.id)
        guild_id = str(ctx.message.guild.id)
        message = deQueue(sender, guild_id)
        await ctx.send(ctx.message.author.mention + ", " +
                       message, delete_after=15)
        await roles(ctx, 10)
        try:
                await ctx.message.delete()
        except:
                pass


@client.command(aliases=["SR"])
async def sr(ctx):
        ''' Prints out the player's saved SR values.
        '''
        try:
                sender = str(ctx.message.author.id)
                guild_id = str(ctx.message.guild.id)
                sr = printPlayerData(sender, guild_id)
                await ctx.send(ctx.message.author.mention + sr)
        except:
                await ctx.send("Error 404: SR doesn't exist",
                               delete_after=25)
        try:
                await ctx.message.delete()
        except:
                pass


@client.command()
async def status(ctx):
        ''' Prints what the sender is queued for.
        '''
        sender = str(ctx.message.author.id)
        guild_id = str(ctx.message.guild.id)
        status = printQueueData(sender, guild_id)
        await ctx.send(ctx.message.author.mention + status,
                       delete_after=25)
        try:
                await ctx.message.delete()
        except:
                pass


##@client.command(aliases=["allsr"])
##async def allSR(ctx):
##        ''' Prints out all the saved SR data.
##        '''
##        try:
##                sr = printAllPlayerData()
##                await ctx.send(sr)
##        except:
##                await ctx.send("Error 404: SR doesn't exist")
##        try:
##                await ctx.message.delete()
##        except:
##                pass
       

@client.command()
async def clear(ctx, amount=5):
        ''' Removes a specified amount of messages.
        '''
        # await ctx.message.delete()
        if amount > 0:
                await ctx.channel.purge(limit=amount+1)


@client.command(aliases=["flip"])
async def coin(ctx):
        ''' Flips a coin.
        '''
        result = random.randint(0,1)
        if result == 0:
                await ctx.send("Heads!")
        else:
                await ctx.send("Tails!")
        try:
                await ctx.message.delete()
        except:
                pass


@client.command()
async def invite(ctx):
        await ctx.send("https://discord.com/api/oauth2/authorize" +
                 "?client_id=707724953352536156&permissions=" +
                 "487976000&scope=bot")
        try:
                await ctx.message.delete()
        except:
                pass
        

## For professionalism, end here.

@client.command(aliases = ["dick", "size"])
async def dicksize(ctx):
        ''' Randomly assigns a number in inches.
        '''
        try:
                await ctx.message.delete()
        except:
                pass
        # await ctx.message.delete()
        i = random.randint(321, 987)
        if str(ctx.message.author) == "Panda#3239":
                i += 2000
                message = "dick?"#str(i/100) + " nanometer dick."
        elif str(ctx.message.author) == "Timmy#3426":
                i += 30
                message = str(i/100) + " inch dick."
        elif str(ctx.message.author) == "Twang#8757":
                i -= 321
                message = str(i/100) + " inch dick."
        elif str(ctx.message.author) == "StodgyMeteor#8420":
                i -= 250
                message = str(i/100) + " inch dick."
        elif str(ctx.message.author) == "Archangel#0346":
                i += 850
                message = str(i/100) + " inch dick."
        elif str(ctx.message.author) == "Aries#0666":
                i -= 321
                message = str(i/100) + " yard dick."
        elif str(ctx.message.author) == "BubbLeS#4835":
                message = "dick beyond human comprehension."
        else:
                message = str(i/100) + " inch dick."
##                await ctx.send(ctx.message.author.mention +
##                               " has a massive dick.")
        #else:
        await ctx.send(ctx.message.author.mention + " has a "
                       + message)


@client.command(aliases=["bi", "pan"])
async def gay(ctx):
        ''' Randomly assigns the user a sexuality. Not always random.
        '''
        try:
                await ctx.message.delete()
        except:
                pass
        # await ctx.message.delete()
        i = random.randint(0,100)
        if str(ctx.message.author) == "Aries#0666":
                await ctx.send(ctx.message.author.mention + " is a mercy main.")
        elif str(ctx.message.author) == "Panda#3239":
                await ctx.send(ctx.message.author.mention + " is bi.")
        elif str(ctx.message.author) == "StodgyMeteor#8420":
                await ctx.send(ctx.message.author.mention + " is a bad torb.")
        else:
                if (i % 11) == 0:
                        await ctx.send(ctx.message.author.mention +
                                       " is gay.")
                elif (i % 11) == 1:
                        await ctx.send(ctx.message.author.mention +
                                       " is straight.")
                elif (i % 11) == 2:
                        await ctx.send(ctx.message.author.mention +
                                       " is asexual.")
                elif (i % 11) == 3:
                        await ctx.send(ctx.message.author.mention +
                                       " is bi.")
                elif (i % 11) == 4:
                        await ctx.send(ctx.message.author.mention +
                                       " is closeted :0.")
                elif (i % 10) == 5:
                        await ctx.send(ctx.message.author.mention +
                                       " is a simp.")
                elif (i % 11) == 6:
                        await ctx.send(ctx.message.author.mention +
                                       " is pan.")
                elif (i % 11) == 7:
                        await ctx.send(ctx.message.author.mention +
                                       " is sexy af.")
                elif (i % 11) == 8:
                        await ctx.send(ctx.message.author.mention +
                                       " will probably die alone :(")
                elif (i % 11) == 9:
                        await ctx.send(ctx.message.author.mention +
                                       " Error 404: Sexuality not found.")
                elif (i % 11) == 10:
                        await ctx.send(ctx.message.author.mention +
                                       " is a furry.")


client.run("token")
