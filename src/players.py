# To get a game started, Patrick will remove themself
# from the following list and add in the real players
# for the game.

class Player():
    def __init__(self, login, name):
        self.login = login
        self.name = name

players = [ Player("nklein","Patrick Stein"), ]

def relevant_player_login(login):
    try:
        return next(filter(lambda p: p.login == login, players))
    except StopIteration:
        return None

def relevant_player_count():
    return len(players)
