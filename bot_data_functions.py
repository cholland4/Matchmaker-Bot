import numpy as np
import json
import random
import requests
from bs4 import BeautifulSoup


def savePlayerData(playerData):
    ''' Saves the hashmap of player data.
    '''
    with open("newdata.json", "w") as f:
        json.dump(playerData, f, indent=4)


def loadPlayerData():
    ''' Loads the hashmap of player data.
    '''
    with open('newdata.json', 'r') as f:
        playerData = json.load(f)
    return playerData


playerData = loadPlayerData()
numQueued = {"tank":0, "dps":0, "support":0}

for player in playerData:
    playerData[player]["queue"] = "none"
    playerData[player]["team"] = -1
savePlayerData(playerData)

def clearQueue():
    ''' Clears the number of players queued and empties the queue.
    '''
    global numQueued
    for player in playerData:
        playerData[playerID]["queue"] = "none"
    savePlayerData(playerData)
    for role in numQueued:
        numQueued[role] = 0
    return numQueued


numQueued = clearQueue()


def queueFor(role, PlayerID):
    ''' Removes the player from the queue
        Sets the player's queued role to whatever they specified.
        Updates number of players queued for each role.
    '''
    if PlayerID not in playerData.keys():
        return("You don't have any stored data.\n")
    global numQueued
    if role in playerData[PlayerID]:
        deQueue(PlayerID)
        playerData[PlayerID]["queue"] = role
        savePlayerData(playerData)
        if role == "tank":
            numQueued["tank"] += 1
            return ("Queued for tank.\n")
        elif role == "damage" or role == "dps":
            numQueued["dps"] += 1
            return ("Queued for dps.\n")
        elif role == "support" or role == "supp":
            numQueued["support"] += 1
            return ("Queued for support.\n")
        elif role == "none":
            deQueue(PlayerID)
            return ("Left the queue.\n")
    else:
        return("Invalid role.\n")


def suppQueued():
    ''' Returns the number of support players needed to fill the queue.
    '''
    if numQueued["support"] < 4:
        numNeeded = 4 - numQueued["support"]
        return str(numNeeded)
    else:
        return 0


def tankQueued():
    ''' Returns the number of tank players needed to fill the queue.
    '''
    if numQueued["tank"] < 4:
        numNeeded = 4 - numQueued["tank"]
        return str(numNeeded)
    else:
        return 0


def adjust(winner):
    ''' Increases the winning team's SR by 100 for the role they queued.
        Decreases the losing team's SR by 100 for the role they queued.
    '''
    global playerData
    playerData = loadPlayerData()
    if(winner != 0):
        for playerID in playerData:
            playerData = loadPlayerData()
            if(playerData[player]["team"] == winner):
                role = playerData[playerID]["queue"]
                playerData[playerID][role] += 50
            elif(playerData[playerID]["team"] != -1):
                role = playerData[playerID]["queue"]
                playerData[playerID][role] -= 50
            playerData[playerID]["team"] = -1
            playerData[playerID]["queue"] = "none"
            savePlayerData(playerData)
    clearQueue()


def dpsQueued():
    ''' Returns the number of dps players needed to fill the queue.
    '''
    if numQueued["dps"] < 4:
        numNeeded = 4 - numQueued["dps"]
        return str(numNeeded)
    else:
        return 0


def allQueued():
    ''' Returns true if all queue conditions are met.
    '''
    if dpsQueued() != 0:
        return False
    if tankQueued() != 0:
        return False
    if suppQueued() != 0:
        return False
    return True


def deQueue(PlayerID):
    ''' Removes the player from the queue.
        Updates number of players queued for each role.
    '''
    global numQueued
    role = playerData[PlayerID]["queue"]
    playerData[PlayerID]["queue"] = "none"
    if role == "tank":
        numQueued["tank"] -= 1
    elif role == "damage" or role == "dps":
        numQueued["dps"] -= 1
    elif role == "support":
        numQueued["support"] -= 1
    elif role == "none":
        return "Not in queue.\n"
    savePlayerData(playerData)
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


def setBtag(btag, PlayerID):
    """ Updates the player's battletag.
    """
    try:
        if PlayerID not in playerData:
            playerData[PlayerID] = {}
        playerData[PlayerID]["btag"] = btag
        savePlayerData(playerData)
        return True
    except:
        return False


def pullSR(PlayerID, playerName):
    """ Updates the player's SR from their online profile.
    """
    try:
        battletag = playerData[PlayerID]["btag"]
        sr_list = webScrape(battletag)
        if sr_list == [-1, -1, -1]:
            return False
        if sr_list[0] != -1:
            setTank(sr_list[0], PlayerID, playerName)
        if sr_list[1] != -1:
            setDamage(sr_list[1], PlayerID, playerName)
        if sr_list[2] != -1:
            setSupport(sr_list[2], PlayerID, playerName)
        return True
    except:
        return False


def setSupport(sr, PlayerID, playerName):
    """ Updates the player's support SR.
    """
    if PlayerID not in playerData:
        playerData[PlayerID] = {}
    sr = int(sr)
    if sr <= 1000 or sr > 5000:
        return False
    try:
        playerData[PlayerID]["support"] = sr
        playerData[PlayerID]["queue"] = "none"
        playerData[PlayerID]["team"] = -1
        if "name" not in playerData[PlayerID].keys():
            playerData[PlayerID]["name"] = playerName
        savePlayerData(playerData)
        return True
    except:
        return False


def setDamage(sr, PlayerID, playerName):
    """ Updates the player's support SR.
    """
    if PlayerID not in playerData:
        playerData[PlayerID] = {}
    sr = int(sr)
    if sr < 1000 or sr > 5000:
        return False
    try:
        playerData[PlayerID]["dps"] = sr
        playerData[PlayerID]["queue"] = "none"
        playerData[PlayerID]["team"] = -1
        if "name" not in playerData[PlayerID].keys():
            playerData[PlayerID]["name"] = playerName
        savePlayerData(playerData)
        return True
    except:
        return False


def setTank(sr, PlayerID, playerName):
    """ Updates the player's support SR.
    """
    if PlayerID not in playerData:
        playerData[PlayerID] = {}
    sr = int(sr)
    if sr < 1000 or sr > 5000:
        return False
    try:
        playerData[PlayerID]["tank"] = sr
        playerData[PlayerID]["queue"] = "none"
        playerData[PlayerID]["team"] = -1
        if "name" not in playerData[PlayerID].keys():
            playerData[PlayerID]["name"] = playerName
        savePlayerData(playerData)
        return True
    except:
        return False


def clearPlayerData():
    ''' Clears playerData of everything.
    '''
    playerData.clear()
    savePlayerData(playerData)
    return playerData


def getPlayerData(PlayerID):
    ''' Returns a specific player's data.
        If possible, should be formatted.
    '''
    pData = loadPlayerData()
    return pData[PlayerID]


def printPlayerData(PlayerID):
    ''' Returns a formatted string with specific user data.
    '''
    pData = getAllPlayerData()
    message = ""
    for key in pData[PlayerID].keys():
        if key == "support":
            message = message + "\nSupport: " + str(pData[PlayerID]["support"])
        elif key == "dps":
            message = message + "\nDPS: " + str(pData[PlayerID]["dps"])
        elif key == "tank":
            message = message + "\nTank: " + str(pData[PlayerID]["tank"])
    if message == "":
        message = "No SR data recorded."
    return message


def printAllPlayerData():
    ''' Returns a formatted string with all user data.
    '''
    playerData = loadPlayerData()
    message = ""
    for PlayerID in playerData.keys():
        message = message + printPlayerData(PlayerID) + "\n\n"
    if message == "":
        message = "No SR data recorded."
    return message


def printQueueData(PlayerID):
    ''' Returns a formatted string about a specific user's queue status.
    '''
    if playerData[PlayerID]["queue"] == "none":
        message = " is not queued!"
    else:
        message = " is queued for: " + playerData[PlayerID]["queue"]
    return message


def printQueue():
    ''' Returns a formatted string with all the users in queue.
    '''
    pData = getAllPlayerData()
    queue = ""
    for playerID in pData.keys():
        if pData[player]["queue"] != "none":
            queue = queue + player[:-5] + ": " + pData[player]["queue"] + "\n"
    if queue == "":
        queue = "Nobody is in queue."
    return queue


def getAllPlayerData():
    ''' Returns all player's data.
        If possible, should be formatted.
    '''
    pData = loadPlayerData()
    return pData

key_queue = "queue"


def getTeam(mmData, teamNum):
    ''' Gets teams.
    '''
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
    ''' Returns a formatted string containing all players for both teams.
    '''
    mmData = mmList[0]
    team1 = getTeam(mmData, 1)
    team2 = getTeam(mmData, 2)
    teamA = "Team 1: Avg = " + str(mmList[1]) + "\n"
    teamB = "Team 2: Avg = " + str(mmList[2]) + "\n"
    
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
        
    message = "```\n" + (teamA) + "\n" + (teamB) + "```"
    return message


def getPlayerTeam(playerID):
    ''' Returns the team number that a specific player is on
    '''
    playerData = loadPlayerData()
    team = str(playerData[playerID]["team"])
    return team


def get_team_id(playerData, teamnum):
    ''' Returns a list of discord user ID tags for members of specified.
    '''
    team_list = []
    for playerID in playerData.keys():
        if playerData[playerID]["team"] == teamnum:
            team_list.append(playerID)
    return team_list