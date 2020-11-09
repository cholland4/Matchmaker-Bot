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



