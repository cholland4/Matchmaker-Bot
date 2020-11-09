class Server:
    def __init__(self, server_id, server_name):
        self.server_id = server_id
        self.name = server_name
        self.draft_channel = None
        self.player_queue = {"tank": [],
                             "dps": [],
                             "support": []}
        self.games_in_progress = []  # append each game object as the mm makes them, and remove each game obj
        #                              as a win is reported

    def __str__(self):
        output = self.name
        return output

    def get_full_queue(self):
        full_queue = []
        for discord_id in self.player_queue["tank"]:
            full_queue.append(discord_id)
        for discord_id in self.player_queue["dps"]:
            full_queue.append(discord_id)
        for discord_id in self.player_queue["support"]:
            full_queue.append(discord_id)

        print("tank:", self.player_queue["tank"])
        print("dps:", self.player_queue["dps"])
        print("supp:", self.player_queue["support"])
        return full_queue

    def remove_from_queue(self, discord_id):
        if discord_id in self.player_queue["tank"]:
            self.player_queue["tank"].remove(discord_id)
        if discord_id in self.player_queue["dps"]:
            self.player_queue["dps"].remove(discord_id)
        if discord_id in self.player_queue["support"]:
            self.player_queue["support"].remove(discord_id)

    def clear_queue(self):
        self.player_queue = {"tank": [],
                             "dps": [],
                             "support": []}


class User:
    def __init__(self, discord_id, username):
        self.discord_id = discord_id
        self.username = username
        self.queue_state = None
        self.tank_sr = None
        self.dps_sr = None
        self.support_sr = None
        self.btag = None

    def __str__(self):
        output = self.username + "\nTank: " + str(self.tank_sr) \
                 + "\nDPS: " + str(self.dps_sr) + "\nSupport: " + str(self.support_sr)
        return output

    def set_sr(self, role, sr):
        if role == "tank":
            self.tank_sr = sr
        if role == "dps":
            self.dps_sr = sr
        if role == "support":
            self.support_sr = sr

    def set_btag(self, btag):
        self.btag = btag

    def queue_for(self, role):
        self.queue_state = role

    def pull_sr(self):
        # webscrape using btag, for loop calling set_sr
        pass


class Game:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def __str__(self):
        pass

    def win(self):
        pass

    def lose(self):
        pass


class Team:
    # users = [user_id...]
    # average = team avg
    # print average and users and their role
    # move users to channels
    #    create/delete channels?
    pass



