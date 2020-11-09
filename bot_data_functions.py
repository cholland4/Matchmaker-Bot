import numpy as np
import json
import pickle
from bot_classes import *
import random
import requests
from bs4 import BeautifulSoup


def load_player_data():
    savefile = open('users.pkl', 'rb')
    try:
        player_data = pickle.load(savefile)
    except EOFError:
        return
    return player_data


def save_player_data(player_data):
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


def add_user(discord_id, discord_name):
    user = User(discord_id, discord_name)
    print("adding user")
    return user


def get_user_by_id(discord_id, discord_name):
    player_data = load_player_data()
    if discord_id in player_data.keys():
        user = player_data[discord_id]
        if discord_name != user.username:
            user.username = discord_name
        return user
    user = add_user(discord_id, discord_name)
    return user


def set_support_sr(discord_id, discord_name, sr):
    player_data = load_player_data()
    if sr < 0 or sr > 5000:
        return False
    user = get_user_by_id(discord_id, discord_name)
    user.support_sr = sr
    player_data[discord_id] = user
    save_player_data(player_data)
    return True


def set_dps_sr(discord_id, discord_name, sr):
    player_data = load_player_data()
    if sr < 0 or sr > 5000:
        return False
    user = get_user_by_id(discord_id, discord_name)
    user.dps_sr = sr
    player_data[discord_id] = user
    save_player_data(player_data)
    return True


def set_tank_sr(discord_id, discord_name, sr):
    player_data = load_player_data()
    if sr < 0 or sr > 5000:
        return False
    user = get_user_by_id(discord_id, discord_name)
    user.tank_sr = sr
    player_data[discord_id] = user
    save_player_data(player_data)
    return True


def print_user(discord_id, discord_name):
    user = get_user_by_id(discord_id, discord_name)
    return str(user)



