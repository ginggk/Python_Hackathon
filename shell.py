from pybcca.tui_helper import run
from core import *
import os


def player_move(player):
    event = input(
        "\n[W] Up \n[D] Right \n[A] Left \n[S] Down \nMove: ").lower()

    if event == "w":
        player.move_north()
        return player
    elif event == "s":
        player.move_south()
        return player
    elif event == "a":
        player.move_west()
        return player
    elif event == "d":
        player.move_east()
        return player
    else:
        print("Invalid move")
        player_move(player)


# def update(key, state):
#     if key == "KEY_UP":


def main():
    os.system('clear')
    map = load_map()
    player = Player(100, {'x': 0, 'y': 0})

    print(map)
    print(player.location)
    player = player_move(player)
    print(player.location)


if __name__ == "__main__":
    main()
