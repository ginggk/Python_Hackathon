class Player:
    def __init__(self, health, location):
        self.health = health
        self.location = location

    def move(self, x, y):
        self.location['x'] += x
        self.location['y'] += y

    def move_north(self):
        self.move(x=0, y=1)

    def move_south(self):
        self.move(x=0, y=-1)

    def move_east(self):
        self.move(x=1, y=0)

    def move_west(self):
        self.move(x=-1, y=0)


class Room:
    def __init__(self, items, enemy):
        self.items = items
        self.enemy = enemy


def player_in_room(player, map):
    return map[player.location['y']][player.location["x"]]


def load_map():
    map = [[0, 0, 0, 0]]
    return map
