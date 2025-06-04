class User:
    def __init__(self, name: str, device_id: str):
        self.name = name
        self.device_id = device_id
        self.predictions = []  # List of dictionaries: [{fight_id:str, winner:str, prediction:str}]

    def __str__(self):
        return f"User(name={self.name}, device_id={self.device_id})"  #TODO: Add predictions output.


class Fight:
    def __init__(self, fight_id: str, fighter1: str, fighter2: str):
        self.fight_id = fight_id
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.winner = None

    def __str__(self):
        return f"Fight(fight_id={self.fight_id}, fighter1={self.fighter1}, fighter2={self.fighter2}, winner={self.winner})"

class FightCard:
    def __init__(self, fights: list[Fight]):
        self.fights = fights

    def __str__(self):
        return f"FightCard(fights={self.fights})"

class Fighter:
    def __init__(self, name: str, height: float, height_in: float, reach: float, leg_reach: float, weight: float, wins: int, losses: int, ncs: int, win_ko: int, win_sub: int, win_dec: int, loss_ko: int, loss_sub: int, loss_dec: int):
        self.name = name
        self.height = height
        self.height_in = height_in
        self.reach = reach
        self.leg_reach = leg_reach
        self.weight = weight
        self.wins = wins
        self.losses = losses
        self.ncs = ncs
        self.win_ko = win_ko
        self.win_sub = win_sub
        self.win_dec = win_dec
        self.loss_ko = loss_ko
        self.loss_sub = loss_sub
        self.loss_dec = loss_dec

    def __str__(self):
        return f"Fighter(name={self.name}, height={self.height}, height_in={self.height_in}, reach={self.reach}, leg_reach={self.leg_reach}, weight={self.weight}, wins={self.wins}, losses={self.losses}, ncs={self.ncs}, win_ko={self.win_ko}, win_sub={self.win_sub}, win_dec={self.win_dec}, loss_ko={self.loss_ko}, loss_sub={self.loss_sub}, loss_dec={self.loss_dec}, win_rate={self.win_rate}, loss_rate={self.loss_rate})"

class Leaderboard:
    def __init__(self, users: list[User]):
        self.users = users

    def __str__(self):
        return f"Leaderboard(users={self.users})"
