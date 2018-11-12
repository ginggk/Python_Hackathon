class Game:
    def __init__(self, player: 'Player', _map) -> None:
        self.player: Player = player
        self._map = _map

    def clear_player_spot(self) -> 'Game':
        self.player = self.player.clear_spot()
        return self

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


class Player:
    def __init__(self, health: int, name: str, location, room) -> None:
        self.health = health
        self.name = name
        self.location = location
        self.room = room

    def clear_spot(self):
        self.room.build[self.location['y']][self.location['x']] = 0
        return self

    def new_spot(self):
        self.room.build[self.location['y']][self.location['x']] = 1
        return self

    def move(self, x, y):
        self.location['x'] += x
        self.location['y'] += y
        return self

    def move_north(self):
        y = self.location['y']
        x = self.location['x']
        place = self.room.build
        if y is not 0:
            if place[y - 1][x] == 0:
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
            if place[y + 1][x] == 0:
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
            if place[y][x + 1] == 0:
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
            if place[y][x - 1] == 0:
                return self.move(x=-1, y=0)
            else:
                return self

        else:
            return self


class Room:
    def __init__(self, items, enemy, build):
        self.items = items
        self.enemy = enemy
        self.build = build


def load_map():
    room_1 = Room([], "enemy", [[2, 2, 2, 2], [2, 0, 1, 2], [2, 0, 2, 2],
                                [2, 0, 2, 2], [2, 0, 4, 3], [2, 2, 2, 2]])
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
