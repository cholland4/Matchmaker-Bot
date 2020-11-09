import numpy as np
import random
from bot_data_functions import *

# Map pool
mapList = ['Blizzard World', 'Busan', 'Dorado',
           'Eichenwalde', 'Hanamura', 'Havana',
           'Hollywood', 'Ilios', 'Junkertown',
           'King\'s Row', 'Lijiang Tower', 'Nepal',
           'Numbani', 'Oasis', 'Rialto',
           'Route 66', 'Temple of Anubis', 'Volskaya Industries',
           'Watchpoint: Gibraltar']


def randomMap():
    i = random.randint(0, 18)
    return mapList[i]


def matchmake(user_data, server_id, server_name):
    if num_queued(server_id, server_name) < 12:
        return [-1, -1]

    roles = split(user_data)

    tank = roles[0]
    dps = roles[1]
    supp = roles[2]

    t = balance(tank)
    d = balance(dps)
    s = balance(supp)

    return combine(user_data, t, d, s)


# ready is a bool
# playerData is a hash table of any number of people
# splits all players into their chosen roles, then selects 4 for each role
def split(user_data):
    tank = []
    dps = []
    supp = []

    for discord_id in user_data.keys():
        role = user_data[discord_id].queue_state
        if role == 'tank':
            tank.append([discord_id, user_data[discord_id].tank_sr])
        elif role == 'dps':
            dps.append([discord_id, user_data[discord_id].dps_sr])
        elif role == 'support':
            supp.append([discord_id, user_data[discord_id].support_sr])

    return [select(tank), select(dps), select(supp)]


# selects 4 players from a pool of any number
# role comes in as a list, returns a list of the randomly selected players
def select(role):
    # print(len(role))
    selected = []
    nums = np.random.choice(len(role), 4, replace=False)
    for i in range(len(nums)):
        selected.append(role[i])
    return selected


# given a role hash table
# add to the value bucket a new entry, Team A or B
# 6 members on A, 6 on B
# as even SR spread as possible
# Assume that role is a list of length 4
def balance(role):
    bestPair = []
    average2 = 0
    bestDifference = 5000
    totalsr = 0
    for i in range(len(role)):
        totalsr += role[i][1]

    for i in range(1, len(role)):
        avg1 = (role[0][1] + role[i][1]) / 2
        avg2 = (totalsr - role[0][1] - role[i][1]) / 2
        difference = avg1 - avg2
        if abs(difference) < abs(bestDifference):
            average2 = avg2
            bestDifference = difference
            bestPair = [avg1, role[0][0], role[i][0]]

    otherPair = [average2]
    for i in range(len(role)):
        if not (role[i][0] in bestPair):
            otherPair.append(role[i][0])

    both = [bestPair, otherPair]
    return both


# list.insert(0, thing-to-insert)
# to prepend things to a list ^^^

# combines the different roles into a team
# average sr is first element in both team A and team B
# good work team


def combine(user_data, tank, dps, supp):
    dReverse = False
    sReverse = False
    tankDiff = tank[0][0] - tank[1][0]
    dpsDiff = dps[0][0] - dps[1][0]
    suppDiff = supp[0][0] - supp[1][0]
    average1 = tank[0][0]
    average2 = tank[1][0]
    #
    # TODO: from this point on, we need the Team and Game classes to be functional
    #
    """
    user_data[tank[0][1]]['team'] = 1
    user_data[tank[0][2]]['team'] = 1
    user_data[tank[1][1]]['team'] = 2
    user_data[tank[1][2]]['team'] = 2

    # brute force calculation of combined sr average
    bestDiff = tankDiff + dpsDiff + suppDiff
    if abs(tankDiff - dpsDiff + suppDiff) < abs(bestDiff):
        bestDiff = tankDiff - dpsDiff + suppDiff
        sReverse = False
        dReverse = True
    if abs(tankDiff + dpsDiff - suppDiff) < abs(bestDiff):
        bestDiff = tankDiff + dpsDiff - suppDiff
        dReverse = False
        sReverse = True
    if abs(tankDiff - dpsDiff - suppDiff) < abs(bestDiff):
        bestDiff = tankDiff - dpsDiff - suppDiff
        dReverse = True
        sReverse = True

    # add to team A or B depending on above calculations
    if dReverse:
        user_data[dps[1][1]]['team'] = 1
        user_data[dps[1][2]]['team'] = 1
        user_data[dps[0][1]]['team'] = 2
        user_data[dps[0][2]]['team'] = 2
        average1 += dps[1][0]
        average2 += dps[0][0]
    else:
        user_data[dps[0][1]]['team'] = 1
        user_data[dps[0][2]]['team'] = 1
        user_data[dps[1][1]]['team'] = 2
        user_data[dps[1][2]]['team'] = 2
        average1 += dps[0][0]
        average2 += dps[1][0]

    if sReverse:
        user_data[supp[1][1]]['team'] = 1
        user_data[supp[1][2]]['team'] = 1
        user_data[supp[0][1]]['team'] = 2
        user_data[supp[0][2]]['team'] = 2
        average1 += supp[1][0]
        average2 += supp[0][0]
    else:
        user_data[supp[0][1]]['team'] = 1
        user_data[supp[0][2]]['team'] = 1
        user_data[supp[1][1]]['team'] = 2
        user_data[supp[1][2]]['team'] = 2
        average1 += supp[0][0]
        average2 += supp[1][0]

    return [user_data, int(average1 / 3), int(average2 / 3)]
    """
    return [-1, -1, -1]


