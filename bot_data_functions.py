import numpy as np
import json
import random
import requests
from bs4 import BeautifulSoup


def create_guild(guild_id):
    allData = loadAllData()
    if guild_id not in allData.keys():
                allData[guild_id] = {}
                allData[guild_id]["server_name"] = None
                allData[guild_id]["vip_list"] = ["176510548702134273"]
                allData[guild_id]["game_status"] = False
                allData[guild_id]["msg"] = None
                allData[guild_id]["response"] = None
                allData[guild_id]["draft_channel"] = None
                allData[guild_id]["t1_channel"] = None
                allData[guild_id]["t2_channel"] = None
                allData[guild_id]["num_queued"] = {"tank":0, "dps":0, "support":0}
                allData[guild_id]["Players"] = {}
    saveAllData(allData)


def set_guild_name(guild_id, guild_name):
    allData[guild_id]["server_name"] = guild_name
    saveAllData(allData)


def delete_guild(guild_id):
    allData = loadAllData()
    allData.pop(guild_id)
    saveAllData(allData)

def create_player(player_id, guild_id):
    allData[guild_id]["Players"][player_id] = {"name": None,
                                               "queue": "none",
                                               "team": -1}
    """
                                               "tank": None,
                                               "dps": None,
                                               "support": None}"""
    saveAllData(allData)

def delete_player(player_id, guild_id):
        allData = loadAllData()
        if player_id in allData[guild_id]["Players"]:
                allData[guild_id]["Players"].pop(player_id)
        saveAllData(allData)


def setChannelID(guild_id, channel_name, channel_id):
        allData[guild_id][channel_name] = int(channel_id)
        saveAllData(allData)

def getChannelID(guild_id, channel_name):
        return allData[guild_id][channel_name]


def setGameStatus(guild_id, new_status):
        allData[guild_id]["game_status"] = new_status
        saveAllData(allData)

def gameStatus(guild_id):
        return allData[guild_id]["game_status"]


def addVip(guild_id, user_id):
        if user_id not in allData[guild_id]["vip_list"]:
                allData[guild_id]["vip_list"].append(user_id)
        saveAllData(allData)

def removeVip(guild_id, user_id):
        if user_id in allData[guild_id]["vip_list"]:
                allData[guild_id]["vip_list"].remove(user_id)
        saveAllData(allData)


def getVipList(guild_id):
        return allData[guild_id]["vip_list"]
                

def saveAllData(allData):
    """ Saves the hashmap of player data.
    """
    with open("data.json", "w") as f:
        json.dump(allData, f, indent=4)


def loadAllData():
    with open('data.json', 'r') as f:
        allData = json.load(f)
    return allData

def savePlayerData(playerData, guild_id):
        allData = loadAllData()
        allData[guild_id]["Players"] = playerData
        saveAllData(allData)

def loadPlayerData(guild_id):
    allData = loadAllData()
    playerData = allData[guild_id]["Players"]
    return playerData

allData = loadAllData()

for guild_id in allData:
    for playerID in allData[guild_id]["Players"]:
        allData[guild_id]["Players"][playerID]["queue"] = "none"
        allData[guild_id]["Players"][playerID]["team"] = -1
saveAllData(allData)

def clearQueue(guild_id):
    """ Clears the number of players queued and empties the queue.
    """
    allData = loadAllData()
    for playerID in allData[guild_id]["Players"]:
        allData[guild_id]["Players"][playerID]["queue"] = "none"
    for role in allData[guild_id]["num_queued"]:
        allData[guild_id]["num_queued"][role] = 0
    saveAllData(allData)


def queueFor(role, PlayerID, guild_id):
    """ Removes the player from the queue
        Sets the player's queued role to whatever they specified.
        Updates number of players queued for each role.
    """
    allData = loadAllData()
    if PlayerID not in allData[guild_id]["Players"].keys():
        create_player(PlayerID, guild_id)
        return("You don't have any stored data.\n")
    #if role in allData[guild_id]["Players"][PlayerID] and \
    if allData[guild_id]["Players"][PlayerID][role] is not None:
        deQueue(PlayerID, guild_id)
        allData = loadAllData()
        allData[guild_id]["Players"][PlayerID]["queue"] = role
        saveAllData(allData)
        if role == "tank":
            allData[guild_id]["num_queued"]["tank"] += 1
            saveAllData(allData)
            return ("Queued for tank.\n")
        elif role == "damage" or role == "dps":
            allData[guild_id]["num_queued"]["dps"] += 1
            saveAllData(allData)
            return ("Queued for dps.\n")
        elif role == "support" or role == "supp":
            allData[guild_id]["num_queued"]["support"] += 1
            saveAllData(allData)
            return ("Queued for support.\n")
        elif role == "none":
            deQueue(PlayerID, guild_id)
            return ("Left the queue.\n")
    else:
        return("Invalid role.\n")


def suppQueued(guild_id):
    """ Returns the number of support players needed to fill the queue.
    """
    allData = loadAllData()
    if allData[guild_id]["num_queued"]["support"] < 4:
        numNeeded = 4 - allData[guild_id]["num_queued"]["support"]
        return str(numNeeded)
    else:
        return 0


def tankQueued(guild_id):
    """ Returns the number of tank players needed to fill the queue.
    """
    allData = loadAllData()
    if allData[guild_id]["num_queued"]["tank"] < 4:
        numNeeded = 4 - allData[guild_id]["num_queued"]["tank"]
        return str(numNeeded)
    else:
        return 0


def adjust(winner, guild_id):
    """ Increases the winning team's SR by 100 for the role they queued.
        Decreases the losing team's SR by 100 for the role they queued.
    """
    allData = loadAllData()
    if(winner != 0):
        for playerID in allData[guild_id]["Players"]:
            allData = loadAllData()
            if(allData[guild_id]["Players"][playerID]["team"] == winner):
                role = allData[guild_id]["Players"][playerID]["queue"]
                allData[guild_id]["Players"][playerID][role] += 50
            elif(allData[guild_id]["Players"][playerID]["team"] != -1):
                role = allData[guild_id]["Players"][playerID]["queue"]
                allData[guild_id]["Players"][playerID][role] -= 50
            allData[guild_id]["Players"][playerID]["team"] = -1
            allData[guild_id]["Players"][playerID]["queue"] = "none"
        else:
            allData[guild_id]["Players"][playerID]["team"] = -1
            allData[guild_id]["Players"][playerID]["queue"] = "none"
    saveAllData(allData)
    clearQueue(guild_id)


def dpsQueued(guild_id):
    """ Returns the number of dps players needed to fill the queue.
    """
    allData = loadAllData()
    if allData[guild_id]["num_queued"]["dps"] < 4:
        numNeeded = 4 - allData[guild_id]["num_queued"]["dps"]
        return str(numNeeded)
    else:
        return 0


def allQueued(guild_id):
    """ Returns true if all queue conditions are met.
    """
    if dpsQueued(guild_id) != 0:
        return False
    if tankQueued(guild_id) != 0:
        return False
    if suppQueued(guild_id) != 0:
        return False
    return True


def deQueue(PlayerID, guild_id):
    """ Removes the player from the queue.
        Updates number of players queued for each role.
    """
    allData = loadAllData()
    role = allData[guild_id]["Players"][PlayerID]["queue"]
    allData[guild_id]["Players"][PlayerID]["queue"] = "none"
    if role == "tank":
        allData[guild_id]["num_queued"]["tank"] -= 1
        saveAllData(allData)
    elif role == "damage" or role == "dps":
        allData[guild_id]["num_queued"]["dps"] -= 1
        saveAllData(allData)
    elif role == "support":
        allData[guild_id]["num_queued"]["support"] -= 1
        saveAllData(allData)
    elif role == "none":
        return "Not in queue.\n"
    saveAllData(allData)
    return "Left the queue.\n"


def webScrape(battletag):
    link = "https://playoverwatch.com/en-us/career/pc/"
    page = requests.get(link + battletag.replace("#", "-"))

    soup = BeautifulSoup(page.text, "html.parser")
    
    ranks = soup.find_all(class_='competitive-rank-role')
    tank = dps = supp = -1

    for i in range(len(ranks)):
        rank_role = ranks[i].find(class_='competitive-rank-role-icon')
        role_sr = ranks[i].find(class_='competitive-rank-level').text
        if "tank" in str(rank_role):
            tank = int(role_sr)
        elif "offense" in str(rank_role):
            dps = int(role_sr)
        elif "support" in str(rank_role):
            supp = int(role_sr)
    return [tank, dps, supp]


def setBtag(btag, PlayerID, guild_id):
    """ Updates the player's battletag.
    """
    allData = loadAllData()
    if PlayerID not in allData[guild_id]["Players"]:
        create_player(PlayerID, guild_id)
    allData[guild_id]["Players"][PlayerID]["btag"] = btag
    saveAllData(allData)
    return True


def pullSR(PlayerID, playerName, guild_id):
    """ Updates the player's SR from their online profile.
    """
    allData = loadAllData()
    try:
        battletag = allData[guild_id]["Players"][PlayerID]["btag"]
        sr_list = webScrape(battletag)
        if sr_list == [-1, -1, -1]:
            return False
        if sr_list[0] != -1:
            setTank(sr_list[0], PlayerID, playerName, guild_id)
        if sr_list[1] != -1:
            setDamage(sr_list[1], PlayerID, playerName, guild_id)
        if sr_list[2] != -1:
            setSupport(sr_list[2], PlayerID, playerName, guild_id)
        return True
    except:
        return False


def setSupport(sr, PlayerID, playerName, guild_id):
    """ Updates the player's support SR.
    """
    allData = loadAllData()
    if PlayerID not in allData[guild_id]["Players"].keys():
        create_player(PlayerID, guild_id)
        allData = loadAllData()
    sr = int(sr)
    if sr <= 1000 or sr > 5000:
        return False
    #try:
    allData[guild_id]["Players"][PlayerID]["support"] = sr
    # allData[guild_id]["Players"][PlayerID]["queue"] = "none"
    allData[guild_id]["Players"][PlayerID]["team"] = -1
    allData[guild_id]["Players"][PlayerID]["name"] = playerName
    saveAllData(allData)
    return True
    #except:
        #saveAllData(allData)
        #return False


def setDamage(sr, PlayerID, playerName, guild_id):
    """ Updates the player's support SR.
    """
    allData = loadAllData()
    print(allData[guild_id]["Players"][PlayerID])
    if PlayerID not in allData[guild_id]["Players"].keys():
        create_player(PlayerID, guild_id)
        allData = loadAllData()
    print(allData[guild_id]["Players"][PlayerID])
    sr = int(sr)
    if sr < 1000 or sr > 5000:
        return False
    allData[guild_id]["Players"][PlayerID]["dps"] = sr
# allData[guild_id]["Players"][PlayerID]["queue"] = "none"
    allData[guild_id]["Players"][PlayerID]["team"] = -1
    allData[guild_id]["Players"][PlayerID]["name"] = playerName
    saveAllData(allData)
    return True
##    except:
##        return False


def setTank(sr, PlayerID, playerName, guild_id):
    """ Updates the player's support SR.
    """
    allData = loadAllData()
    if PlayerID not in allData[guild_id]["Players"].keys():
        create_player(PlayerID, guild_id)
        allData = loadAllData()
    sr = int(sr)
    if sr < 1000 or sr > 5000:
        return False
##    try:
    allData[guild_id]["Players"][PlayerID]["tank"] = sr
        # allData[guild_id]["Players"][PlayerID]["queue"] = "none"
    allData[guild_id]["Players"][PlayerID]["team"] = -1
    allData[guild_id]["Players"][PlayerID]["name"] = playerName
    saveAllData(allData)
    return True
##    except:
##        return False


def clearPlayerData(guild_id):
    """ Clears playerData of everything.
    """
    allData = loadAllData()
    allData[guild_id]["Players"].clear()
    saveAllData(allData)
    return allData


def getPlayerData(PlayerID, guild_id):
    """ Returns a specific player's data.
        If possible, should be formatted.
    """
    pData = loadPlayerData(guild_id)
    return pData[PlayerID]


def printPlayerData(PlayerID, guild_id):
    """ Returns a formatted string with specific user data.
    """
    pData = getPlayerData(PlayerID, guild_id)
    t_message = ""
    d_message = ""
    s_message = ""
    for key in pData.keys():
        if key == "support":
            s_message = "\nSupport: " + str(pData["support"])
        elif key == "dps":
            d_message = "\nDPS: " + str(pData["dps"])
        elif key == "tank":
            t_message = "\nTank: " + str(pData["tank"])
    message = t_message + d_message + s_message
    if message == "":
        message = "No SR data recorded."
    return message


def printAllPlayerData(guild_id):
    """ Returns a formatted string with all user data.
    """
    playerData = loadPlayerData(guild_id)
    message = ""
    for PlayerID in playerData.keys():
        message = message + printPlayerData(PlayerID) + "\n\n"
    if message == "":
        message = "No SR data recorded."
    return message


def printQueueData(PlayerID, guild_id):
    """ Returns a formatted string about a specific user's queue status.
    """
    allData = loadAllData()
    if allData[guild_id]["Players"][PlayerID]["queue"] == "none":
        message = " is not queued!"
    else:
        message = " is queued for: " + allData[guild_id]["Players"][PlayerID]["queue"]
    return message


def printQueue(guild_id):
    """ Returns a formatted string with all the users in queue.
    """
    pData = getAllPlayerData(guild_id)
    queue = ""
    for playerID in pData.keys():
        if pData[playerID]["queue"] != "none":
            queue = queue + pData[playerID]["name"][:-5] + \
                    ": " + pData[playerID]["queue"] + "\n"
    if queue == "":
        queue = "Nobody is in queue."
    return queue


def getAllPlayerData(guild_id):
    """ Returns all player's data.
        If possible, should be formatted.
    """
    pData = loadPlayerData(guild_id)
    return pData

key_queue = "queue"
# I got this far with rewriting playerData with allData or allData[guild_id]["Players"]

def getTeam(mmData, teamNum):
    """ Gets teams.
    """
    team = {}
    tanks = {}
    dps = {}
    numSupp = 0
    numDPS = 0
    for playerID in mmData.keys():
        if mmData[playerID]["team"] == teamNum:
            if mmData[playerID]["queue"] == "tank":
                tanks[playerID] = mmData[playerID]["queue"]
            elif mmData[playerID]["queue"] == "dps":
                dps[playerID] = mmData[playerID]["queue"]
            else:
                team[playerID] = mmData[playerID]["queue"]
    team.update(dps)
    team.update(tanks)
    return team


def printTeams(mmList):
    """ Returns a formatted string containing all players for both teams.
    """
    mmData = mmList[0]
    team1 = getTeam(mmData, 1)
    team2 = getTeam(mmData, 2)
    teamA = "Team 1: Avg = " + str(mmList[1]) + "\n"
    teamB = "Team 2: Avg = " + str(mmList[2]) + "\n"
    teamDiff = "\n\nTeam Difference" + str(abs(mmList[1] - mmList[2]))
    
    for playerID in team1.keys():
        playerName = mmData[playerID]["name"]
        teamA = teamA + playerName + \
                (" " * (32-len(playerName))) + mmData[playerID]["queue"] + \
                "\n"
        
    for playerID in team2.keys():
        playerName = mmData[playerID]["name"]
        teamB = teamB + playerName + \
                (" " * (32-len(playerName))) + mmData[playerID]["queue"] + \
                "\n"
        
    message = "```\n" + (teamA) + "\n" + (teamB) + teamDiff + "```"
    return message


def getPlayerTeam(playerID, guild_id):
    """ Returns the team number that a specific player is on
    """
    playerData = loadPlayerData(guild_id)
    team = str(playerData[playerID]["team"])
    return team


def get_team_id(playerData, teamnum, guild_id):
    """ Returns a list of discord user ID tags for members of specified.
    """
    allData = loadAllData()
    team_list = []
    for playerID in allData[guild_id]["Players"].keys():
        if allData[guild_id]["Players"][playerID]["team"] == teamnum:
            team_list.append(playerID)
    return team_list
=======
import numpy as np
import json
import pickle
from bot_classes import *
import random
import requests
from bs4 import BeautifulSoup


def load_user_data():
    savefile = open('users.pkl', 'rb')
    try:
        user_data = pickle.load(savefile)
    except EOFError:
        return
    return user_data


def save_user_data(player_data):
    pickle.dump(player_data, open("users.pkl", "wb"))


def load_server_data():
    savefile = open('servers.pkl', 'rb')
    try:
        server_data = pickle.load(savefile)
    except EOFError:
        return
    return server_data


def save_server_data(server_data):
    pickle.dump(server_data, open("servers.pkl", "wb"))


def add_server(server_id, server_name):
    server_data = load_server_data()
    # server_data = {}
    server = Server(server_id, server_name)
    server_data[server_id] = server
    save_server_data(server_data)
    print("adding server", server_name)
    return server


def remove_server(server_id):
    server_data = load_server_data()
    server_data.pop(server_id)
    save_server_data(server_data)


def get_server_by_id(server_id, server_name):
    server_data = load_server_data()
    if server_id in server_data.keys():
        server = server_data[server_id]
        if server_name != server.name and server_name is not None:
            server.name = server_name
            save_server_data(server_data)
        return server
    server = add_server(server_id, server_name)
    return server


def add_user(discord_id, discord_name):
    player_data = load_user_data()
    user = User(discord_id, discord_name)
    player_data[discord_id] = user
    save_user_data(player_data)
    print("adding user")
    return user


def get_user_by_id(discord_id, discord_name):
    user_data = load_user_data()
    if discord_id in user_data.keys():
        user = user_data[discord_id]
        if discord_name != user.username and discord_name is not None:
            user.username = discord_name
            save_user_data(user_data)
        return user
    user = add_user(discord_id, discord_name)
    return user


def set_battletag(discord_id, discord_name, btag):
    user_data = load_user_data()
    user = get_user_by_id(discord_id, discord_name)
    user.btag = btag
    user_data[discord_id] = user
    save_user_data(user_data)
    return True


def set_support_sr(discord_id, discord_name, sr):
    user_data = load_user_data()
    if sr < 0 or sr > 5000:
        return False
    user = get_user_by_id(discord_id, discord_name)
    user.support_sr = sr
    user_data[discord_id] = user
    save_user_data(user_data)
    return True


def set_dps_sr(discord_id, discord_name, sr):
    user_data = load_user_data()
    if sr < 0 or sr > 5000:
        return False
    user = get_user_by_id(discord_id, discord_name)
    user.dps_sr = sr
    user_data[discord_id] = user
    save_user_data(user_data)
    return True


def set_tank_sr(discord_id, discord_name, sr):
    user_data = load_user_data()
    if sr < 0 or sr > 5000:
        return False
    user = get_user_by_id(discord_id, discord_name)
    user.tank_sr = sr
    user_data[discord_id] = user
    save_user_data(user_data)
    return True


def print_user(discord_id, discord_name):
    user = get_user_by_id(discord_id, discord_name)
    return str(user)


def queueFor(discord_id, discord_name, server_id, server_name, role):
    ''' Removes the player from the queue
        Sets the player's queued role to whatever they specified.
        Updates number of players queued for each role.
    '''
    server_data = load_server_data()
    user_data = load_user_data()
    if discord_id not in user_data.keys():
        add_user(discord_id, discord_name)
        return "You don't have any stored data.\n"
    if server_id not in server_data.keys():
        add_server(server_id, server_name)
        server_data = load_server_data()
    user = get_user_by_id(discord_id, discord_name)
    server = get_server_by_id(server_id, server_name)
    if role == "supp":
        role = "support"
    elif role == "damage":
        role = "dps"

    user.queue_state = role
    # print(user.queue_state)
    server.remove_from_queue(discord_id)
    server.player_queue[role].append(discord_id)
    user_data[discord_id] = user
    server_data[server_id] = server
    # print(server.get_full_queue())
    save_user_data(user_data)
    save_server_data(server_data)
    if role == "tank":
        return "Queued for tank.\n"
    elif role == "dps":
        return "Queued for dps.\n"
    elif role == "support":
        return "Queued for support.\n"
    elif role is None:
        return "Left the queue.\n"
    else:
        return "Invalid role.\n"


def deQueue(discord_id, discord_name, server_id, server_name):
    ''' Removes the player from the queue.
        Updates number of players queued for each role.
    '''
    server_data = load_server_data()
    user_data = load_user_data()
    if discord_id not in user_data.keys():
        add_user(discord_id, discord_name)
        return "you don't have any stored data.\n"
    if server_id not in server_data.keys():
        add_server(server_id, server_name)
        server_data = load_server_data()
    user = get_user_by_id(discord_id, discord_name)
    server = get_server_by_id(server_id, server_name)
    role = user.queue_state
    server.remove_from_queue(discord_id)
    user.queue_state = None
    save_user_data(user_data)
    if role is None:
        return "not in queue.\n"
    server_data[server_id] = server
    save_server_data(server_data)
    return "left the queue.\n"


def clear_queue(server_id, server_name):
    server_data = load_server_data()
    if server_id not in server_data.keys():
        add_server(server_id, server_name)
        server_data = load_server_data()
    server = get_server_by_id(server_id, server_name)
    server.clear_queue()
    server_data[server_id] = server
    save_server_data(server_data)
    return "cleared the queue.\n"


def num_queued(server_id, server_name):
    server_data = load_server_data()
    if server_id not in server_data.keys():
        add_server(server_id, server_name)
        server_data = load_server_data()
    server = get_server_by_id(server_id, server_name)
    num_tanks = len(server.player_queue["tank"])
    num_dps = len(server.player_queue["dps"])
    num_supp = len(server.player_queue["support"])
    return [num_tanks, num_dps, num_supp]


def printQueue(server_id, server_name):
    ''' Returns a formatted string with all the users in queue.
    '''
    server_data = load_server_data()
    user_data = load_user_data()
    if server_id not in server_data.keys():
        add_server(server_id, server_name)
        server_data = load_server_data()
    server = get_server_by_id(server_id, server_name)
    queue = ""
    for discord_id in server.get_full_queue():
        print(discord_id, user_data[discord_id].queue_state)
        if user_data[discord_id].queue_state is not None:
            queue = queue + user_data[discord_id].username[:-5] + \
                    ": " + user_data[discord_id].queue_state + "\n"
    if queue == "":
        queue = "Nobody is in queue."
    return queue
