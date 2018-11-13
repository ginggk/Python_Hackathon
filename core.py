class Game:
    def __init__(self, player: 'Player', _map, state) -> None:
        self.player: Player = player
        self._map = _map
        self.state = state
        self.enemy = None

    def clear_player_spot(self) -> 'Game':
        self.player = self.player.clear_spot()
        return self

    def player_check_space(self, direction):
        return self.player.check_space(direction)

    def player_new_spot(self) -> "Game":
        self.player = self.player.new_spot()
        return self

    def move_player_north(self) -> 'Game':
        self.player = self.player.move_north()
        return self

    def move_player_south(self) -> 'Game':
        self.player = self.player.move_south()
        return self

    def move_player_west(self) -> 'Game':
        self.player = self.player.move_west()
        return self

    def move_player_east(self) -> 'Game':
        self.player = self.player.move_east()
        return self

    def player_check_for_enemy(self, enemies):
        return self.player.check_for_enemy(enemies)

    def player_attack(self):
        return self.player.attack(self.enemy)


class Player:
    def __init__(self, health: int, name: str, magic, location, room) -> None:
        self.health = health
        self.name = name
        self.magic = magic
        self.base_attack = 5
        self.weapon = "None"
        self.spell = "None"
        self.armor = "None"
        self.location = location
        self.room = room
        self.inventory = {
            'gold': 0,
            'weapons': [],
            'armors': [],
            'spell-book': [],
            'items': {
                'keys': [],
                'potions': []
            }
        }

    def attack(self, enemy):
        attack = (self.base_attack * self.weapon['multiplier'])
        enemy.health -= (attack - enemy.armor['defense'])
        return self

    def clear_spot(self):
        self.room.build[self.location['y']][self.location['x']] = 0
        return self

    def new_spot(self):
        self.room.build[self.location['y']][self.location['x']] = 1
        return self

    #checks the direction from the player using
    # 'north', 'east', 'south', or 'west'
    # to return a string value of what is there
    def check_space(self, direction):
        y = self.location['y']
        x = self.location['x']
        place = self.room.build

        if direction == "north":
            if place[y - 1][x] == 4:
                return "enemy"
        elif direction == "south":
            if place[y + 1][x] == 4:
                return 'enemy'
        elif direction == "east":
            if place[y][x + 1] == 4:
                return 'enemy'
        elif direction == "west":
            if place[y][x - 1] == 4:
                return 'enemy'

    def check_for_enemy(self, enemies):
        for enemy in enemies:
            if self.location['x'] == enemy.location['x'] and self.location[
                    'y'] == enemy.location['y'] and enemy.is_dead() == False:
                return enemy
            else:
                return None

    def move(self, x, y):
        self.location['x'] += x
        self.location['y'] += y
        return self

    def move_north(self):
        y = self.location['y']
        x = self.location['x']
        place = self.room.build
        if y is not 0:
            if place[y - 1][x] == 0 or place[y - 1][x] == 4:
                return self.move(x=0, y=-1)
            else:
                return self
        else:
            return self

    def move_south(self):
        y = self.location['y']
        x = self.location['x']
        place = self.room.build
        if y is not len(place) - 1:
            if place[y + 1][x] == 0 or place[y + 1][x] == 4:
                return self.move(x=0, y=1)
            else:
                return self
        else:
            return self

    def move_east(self):
        y = self.location['y']
        x = self.location['x']
        place = self.room.build
        if x is not len(place[y]) - 1:
            if place[y][x + 1] == 0 or place[y][x + 1] == 4:
                return self.move(x=1, y=0)
            else:
                return self
        else:
            return self

    def move_west(self):
        y = self.location['y']
        x = self.location['x']
        place = self.room.build
        if x is not 0:
            if place[y][x - 1] == 0 or place[y][x - 1] == 4:
                return self.move(x=-1, y=0)
            else:
                return self

        else:
            return self


class Enemy:
    def __init__(self, name, health, magic, weapon, spell, armor, location):
        self.name = name
        self.health = health
        self.magic = magic
        self.weapon = weapon
        self.spell = spell
        self.armor = armor
        self.location = location
        self.dead = False

    def is_dead(self):
        if self.health <= 0:
            self.health = 0
            return True
        else:
            return False


class Room:
    def __init__(self, items, enemies, build):
        self.items = items
        self.enemies = enemies
        self.build = build


def load_armor():
    none = {'name': "none", 'defense': 0}
    armors = [none]
    return armors


def get_armor(name):
    armors = load_armor()
    for armor in armors:
        if armor['name'] == name:
            return armor
        else:
            break


def load_weapons():
    none = {'name': 'none', 'multiplier': 1, 'sharpness': 0}
    weapons = [none]
    return weapons


def get_weapon(name):
    weapons = load_weapons()
    for weapon in weapons:
        if weapon['name'] == name:
            return weapon


def load_map():

    room_1 = Room([], [
        Enemy("Ginger", 100, 100, get_weapon('none'), "None",
              get_armor('none'), {
                  'x': 2,
                  'y': 4
              })
    ], [[2, 2, 2, 2], [2, 0, 1, 2], [2, 0, 2, 2], [2, 0, 2, 2], [2, 0, 4, 3],
        [2, 2, 2, 2]])
    _map = [room_1]
    return _map


def draw_room(room):
    string = ''
    for i in room:
        if i == 0:
            string += " "
        elif i == 1:
            string += "P"
        elif i == 2:
            string += "[]"
        elif i == 3:
            string += "E"
        elif i == 4:
            string += "X"
    return string
