from random import randrange


class Game:
    def __init__(self, player: 'Player', _map, state) -> None:
        self.player: Player = player
        self._map = _map
        self.map_index = 0
        self.state = state
        self.enemy = None
        self.battle_log: list = []

    def fix_log_length(self):
        if len(self.battle_log) > 6:
            del self.battle_log[0]
        return self

    #adds the battle message to the battle log while keeping it a decent size
    def update_battle_log(self, action):
        enemy = self.enemy
        enemy_attack_msg = '{} attacked you\n'.format(enemy.name)
        player_attack_msg = 'You attacked {}'.format(enemy.name)
        enemy_cast_msg = '{} casted {}\n'.format(enemy.name,
                                                 enemy.spell['name'])
        player_cast_msg = 'You casted {}'.format(self.player.spell['name'])

        if action == 'enemy-attack':
            self.battle_log.append(enemy_attack_msg)
        elif action == 'player-attack':
            self.battle_log.append(player_attack_msg)
        elif action == 'enemy-cast':
            self.battle_log.append(enemy_cast_msg)
        elif action == 'player-cast':
            self.battle_log.append(player_cast_msg)

        self.fix_log_length()
        return self

    def clear_player_spot(self) -> 'Game':
        self.player = self.player.clear_spot()
        return self

    def player_check_space(self, direction):
        return self.player.check_space(direction)

    def player_new_spot(self) -> "Game":
        self.player = self.player.new_spot()
        return self

    def player_move_direction(self, direction):
        return self.player.move_in_direction(direction)

    def player_check_for_enemy(self, enemies):
        return self.player.check_for_enemy(enemies)


class Item:
    def __init__(self, name, classify):
        self.name = name
        self.classify = classify


class Player:
    def __init__(self, health: int, name: str, magic, location, room) -> None:
        self.health = health
        self.name = name
        self.magic = magic
        self.base_attack = 5
        self.weapon = "None"
        self.spell = {'name': 'Firepuff', 'cost': 10}
        self.armor = "none"
        self.location = location
        self.room = room
        self.inventory = {
            'gold':
            0,
            'weapons': [],
            'armors': [],
            'spell-book': [
                {
                    'name': 'Firepuff',
                    'cost': 10
                },
                {
                    'name': "Ice-Chill",
                    'cost': 10
                },
            ],
            'items': {
                'keys': [],
                'potions': []
            }
        }

    def is_dead(self):
        if self.health <= 0:
            self.health = 0
            return True
        else:
            return False

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
            if place[y - 1][x] == 3:
                return "exit"
            elif place[y - 1][x] == 5:
                return "entrance"
        elif direction == "south":
            if place[y + 1][x] == 3:
                return 'exit'
            elif place[y + 1][x] == 5:
                return "entrance"
        elif direction == "east":
            if place[y][x + 1] == 3:
                return 'exit'
            elif place[y][x + 1] == 5:
                return "entrance"
        elif direction == "west":
            if place[y][x - 1] == 3:
                return 'exit'
            elif place[y][x - 1] == 5:
                return "entrance"

    def check_for_enemy(self, enemies):
        for enemy in enemies:
            if self.location['x'] == enemy.location['x'] and self.location[
                    'y'] == enemy.location['y'] and enemy.is_dead() == False:
                return enemy
            else:
                return None

    def move_in_direction(self, direction):
        if direction == 'north':
            self.move_north()
        elif direction == 'south':
            self.move_south()
        elif direction == 'east':
            self.move_east()
        elif direction == 'west':
            self.move_west()

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
    def __init__(self, name, health, magic, base_attack, weapon, spell, armor,
                 location):
        self.name = name
        self.health = health
        self.magic = magic
        self.base_attack = base_attack
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
    def __init__(self, player_start, through_exit, enemies, build):
        self.player_start = player_start  #determines where the player when the room is displayed
        self.through_exit = through_exit  #determines where the player is if they go come back through the exit door
        self.enemies = enemies
        self.build = build


def load_map():

    room_1 = build_room_1()
    room_2 = build_room_2()
    _map = [room_1, room_2]
    return _map


[
    1,
    2,
    3,
]


def build_room_1():
    start = {'x': 2, 'y': 1}

    _exit = {'x': 2, 'y': 4}

    enemies = [
        Enemy("Ginger", 100, 100, 5, get_weapon('none'), {
            'name': 'Firepuff',
            'cost': 10
        }, get_armor('none'), {
            'x': 2,
            'y': 4
        })
    ]

    build = [
        [2, 2, 2, 2],
        [2, 0, 1, 2],
        [2, 0, 2, 2],
        [2, 0, 2, 2],
        [2, 0, 4, 3],
        [2, 2, 2, 2],
    ]

    room = Room(start, _exit, enemies, build)
    return room


def build_room_2():
    start = {'x': 1, 'y': 2}

    _exit = {'x': 0, 'y': 0}

    enemies = []

    build = [
        [2, 2, 2, 2, 2, 2],
        [2, 2, 0, 0, 0, 2],
        [5, 0, 0, 0, 0, 2],
        [2, 2, 0, 0, 4, 2],
        [2, 2, 2, 2, 3, 2],
    ]

    room = Room(start, _exit, enemies, build)
    return room


def load_armor():
    none = {'name': "none", 'defense': 0}
    leather = {'name': "Leather", 'defense': 1}
    armors = [none, leather]
    return armors


def get_armor(name):
    armors = load_armor()
    for armor in armors:
        if armor['name'] == name:
            return armor


def load_weapons():
    none = {'name': 'none', 'multiplier': 1, 'sharpness': 0}
    broken_dagger = {'name': 'Broken Dagger', 'multiplier': 1.2}
    weapons = [none, broken_dagger]
    return weapons


def get_weapon(name):
    weapons = load_weapons()
    for weapon in weapons:
        if weapon['name'] == name:
            return weapon


def attack(player, enemy):
    attack = (player.base_attack * player.weapon['multiplier'])
    enemy.health -= (attack - enemy.armor['defense'])
    return player


def load_spells():
    firepuff = {'name': 'Firepuff', 'cost': 10}
    ice_chill = {'name': "Ice-Chill", 'cost': 10}


def enemy_decision(enemy, player, state):
    num = randrange(0, 10)
    if enemy.magic > enemy.spell['cost'] and num < 5:
        cast_spell(enemy, player)
        state.update_battle_log('enemy-cast')
    else:
        attack(enemy, player)
        state.update_battle_log('enemy-attack')


def cast_spell(player, enemy):
    if player.spell[
            'name'] == 'Firepuff' and player.magic >= player.spell['cost']:
        enemy.health -= randrange(5, 10)
        player.magic -= player.spell['cost']
    elif player.spell[
            'name'] == "Ice-Chill" and player.magic >= player.spell['cost']:
        enemy.health -= 8
        player.magic -= player.spell['cost']


def equip_weapon(player, index):
    if index <= len(player.inventory['weapons']):
        player.weapon = player.inventory['weapons'][index - 1]


def equip_armor(player, index):
    if index <= len(player.inventory['armors']):
        player.armor = player.inventory['armors'][index - 1]


def equip_spell(player, index):
    if index <= len(player.inventory['spell-book']):
        player.spell = player.inventory['spell-book'][index - 1]
