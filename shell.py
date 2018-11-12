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


def view(state, x, y):
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


def main():
    os.system('clear')
    _map = load_map()
    name = input("What is your name: ")
    player = Player(100, name, {'x': 2, 'y': 1}, _map[0])

    run(Game(player, _map), update, view)


if __name__ == "__main__":
    main()
