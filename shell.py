from pybcca.tui_helper import run
from core import *
import os

# def player_move(player):
#     event = input(
#         "\n[W] Up \n[D] Right \n[A] Left \n[S] Down \nMove: ").lower()

#     if event == "w":
#         player.move_north()
#         return player
#     elif event == "s":
#         player.move_south()
#         return player
#     elif event == "a":
#         player.move_west()
#         return player
#     elif event == "d":
#         player.move_east()
#         return player
#     else:
#         print("Invalid move")
#         player_move(player)


def update(key, state: Game) -> Game:
    if state.state == "explore":
        if key == "KEY_UP":
            state.clear_player_spot()
            state.move_player_north()
            state.player_new_spot()
            return state
        elif key == "KEY_DOWN":
            state.clear_player_spot()
            state.move_player_south()
            state.player_new_spot()
            return state
        elif key == "KEY_LEFT":
            state.clear_player_spot()
            state.move_player_west()
            state.player_new_spot()
            return state
        elif key == "KEY_RIGHT":
            state.clear_player_spot()
            state.move_player_east()
            state.player_new_spot()
            return state
        else:
            return state
    # elif state.state = "battle":

    return state


def explore_view(state, x, y):
    string = f'Use the Arrow keys to move\nPlayer: {state.player.name}\n\n\t'
    for row in state.player.room.build:
        for cell in row:
            if cell == 0:
                string += "   "
            elif cell == 1:
                string += " P "
            elif cell == 2:
                string += "|W|"
            elif cell == 3:
                string += " E "
            elif cell == 4:
                string += " X "
        string += "\n\t"
    return string


def battle_view(state, x, y):
    player = state.player
    enemy = player.room.enemy
    space = ""

    string = '\t|| {:6} || {:<10} || {} ||\n\tHealth: {}{:<13}Health: {}'.format(
        player.name, space, enemy.name, player.health, space, enemy.health)
    return string


def view(state, x, y):
    if state.state == "explore":
        string = explore_view(state, x, y)
    elif state.state == "battle":
        string = battle_view(state, x, y)
    return string


def player_name():

    name = input("What is your name: ")
    if len(name) == 0:
        player_name()

    else:
        return name


def main():
    os.system('clear')
    _map = load_map()
    name = player_name()
    player = Player(100, name, {'x': 2, 'y': 1}, _map[0])

    run(Game(player, _map, "explore"), update, view)


if __name__ == "__main__":
    main()
