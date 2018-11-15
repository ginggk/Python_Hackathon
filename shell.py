from pybcca.tui_helper import run
from core import *
import os


def check_space_action(state, direction):
    if state.player_check_space(direction) == 'exit':
        state.state = 'explore'
        change_room(state, 'exit')
        return state
    elif state.player_check_space(direction) == 'entrance':
        state.state = 'explore'
        change_room(state, 'entrance')
        return state
    else:
        state.player_move_direction(direction)


def change_room(state, door_type):
    if door_type == "exit":
        state.map_index += 1
        index = state.map_index
        state.player.room = state._map[index]
        state.player.location = state.player.room.player_start
    elif door_type == "entrance":
        state.map_index -= 1
        index = state.map_index
        state.player.room = state._map[index]
        state.player.location = state.player.room.through_exit


def on_enemy_space_action(state):
    enemies = state.player.room.enemies
    enemy = state.player_check_for_enemy(enemies)
    if enemy is not None:
        state.state = 'battle'
        state.enemy = enemy
    return state


def explore_update(key, state: Game) -> Game:
    if key == "KEY_UP":
        state.clear_player_spot()
        check_space_action(state, 'north')
        state.player_new_spot()
        on_enemy_space_action(state)

        return state
    elif key == "KEY_DOWN":
        state.clear_player_spot()
        check_space_action(state, 'south')
        state.player_new_spot()
        on_enemy_space_action(state)
        return state
    elif key == "KEY_LEFT":
        state.clear_player_spot()
        check_space_action(state, 'west')
        state.player_new_spot()
        on_enemy_space_action(state)
        return state
    elif key == "KEY_RIGHT":
        state.clear_player_spot()
        check_space_action(state, 'east')
        on_enemy_space_action(state)
        state.player_new_spot()

        return state
    else:
        return state
    return state


def battle_update(key, state: Game) -> Game:
    if key == "1":
        attack(state.player, state.enemy)
        state.update_battle_log('player-attack')
        enemy_decision(state.enemy, state.player, state)
    elif key == "2":
        cast_spell(state.player, state.enemy)
        state.update_battle_log('player-cast')
        enemy_decision(state.enemy, state.player, state)

    elif key == "3":
        rest(state.player)
        state.update_battle_log('player-rest')
        enemy_decision(state.enemy, state.player, state)
    elif key == "4":
        state.state = "weapon_menu"
    elif key == '5':
        state.state = 'armor_menu'
    elif key == '6':
        state.state = 'spell_menu'

    if state.enemy.is_dead():
        state.state = 'loot_menu'
    elif state.player.is_dead():
        state.state = 'game-over'
    return state


def weapon_menu_update(key, state):
    if key == "1":
        equip_weapon(state.player, 1)
        state.state = "battle"
    elif key == "2":
        equip_weapon(state.player, 2)
        state.state = "battle"
    return state


def armor_menu_update(key, state):
    if key == '1':
        equip_armor(state.player, 1)
        state.state = "battle"
    elif key == '2':
        equip_armor(state.player, 2)
        state.state = 'battle'
    return state


def spell_menu_update(key, state):
    if key == '1':
        equip_spell(state.player, 1)
        state.state = 'battle'
    elif key == "2":
        equip_spell(state.player, 2)
        state.state = 'battle'
    return state


def game_over_update(key, state):
    return state


def loot_update(key, state):
    if key == '1':
        loot(state.player, state.enemy, 1)
    elif key == '2':
        loot(state.player, state.enemy, 2)
    elif key == "3":
        loot(state.player, state.enemy, 3)
    elif key == "4":
        loot(state.player, state.enemy, 4)
    elif key == "s":
        state.state = "remove_inventory_menu"
    elif key == "d":
        state.state = "explore"
    return state


def update(key, state: Game) -> Game:
    if state.state == "explore":
        state = explore_update(key, state)
    elif state.state == "battle":
        state = battle_update(key, state)
    elif state.state == "weapon_menu":
        state = weapon_menu_update(key, state)
    elif state.state == 'armor_menu':
        state = armor_menu_update(key, state)
    elif state.state == 'spell_menu':
        state = spell_menu_update(key, state)
    elif state.state == 'game-over':
        state = game_over_update(key, state)
    elif state.state == 'loot_menu':
        state = loot_update(key, state)

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
                string += "[ ]"
            elif cell == 4:
                string += " X "
            elif cell == 5:
                string += "[ ]"
        string += "\n\t"
    return string


def battle_view(state, x, y):
    player = state.player
    enemy = state.enemy
    space = ""

    string = ''

    str_names = '\t|| {:6} || {:<10} || {} ||'.format(player.name, space,
                                                      enemy.name)
    str_health = '\n\tHealth: {:.2f}{:<10}Health: {:.2f}'.format(
        player.health, space, enemy.health)
    str_magic = '\n\tMagic Core: {:<3}{:<9}Magic Core: {:<3}'.format(
        player.magic, space, enemy.magic)
    str_weapons = '\n\tWeapon: {:<13}{:<3}Weapon: {:<13}'.format(
        player.weapon['name'], space, enemy.weapon['name'])
    str_spell = '\n\tSpell: {:<13}{:<4}Spell: {:<13}'.format(
        player.spell['name'], space, enemy.spell['name'])
    str_armor = '\n\tArmor: {:<13}{:<4}Armor: {:<13}'.format(
        player.armor['name'], space, enemy.armor['name'])

    str_battle_log = '\n\n\tBattle Log\n'
    for i in state.battle_log:
        str_battle_log += i + '\n'

    return string + str_names + str_health + str_magic + str_weapons + str_spell + str_armor + str_battle_log


def weapon_menu_view(state, x, y):
    string = 'Choose Your Current Weapon\n'
    counter = 1

    for weapon in state.player.inventory['weapons']:
        new_str = f'{counter}: {weapon["name"]}\n'
        counter += 1
        string += new_str
    return string


def armor_menu_view(state, x, y):
    string = 'Choose Your Current Armor\n'
    counter = 1

    for armor in state.player.inventory['armors']:
        new_str = f'{counter}: {armor["name"]}\n'
        counter += 1
        string += new_str
    return string


def spell_menu_view(state, x, y):
    string = "Choose a Spell to Equip\n"
    counter = 1

    for spell in state.player.inventory['spell-book']:
        new_str = f'{counter}: {spell["name"]}\n'
        counter += 1
        string += new_str
    return string


def game_over_view(state, x, y):
    string = "Game Over, You Died"
    return string


def loot_view(state, x, y):
    string = "Choose what items you would like to take\n\n"
    gold = f"[1] Gold: {state.enemy.loot[0]['value']}\n"
    weapon = f"[2] Weapon: {state.enemy.loot[1]['name']}\n"
    armor = f"[3] Armor: {state.enemy.loot[2]['name']}\n"

    return string + gold + weapon + armor + inv


def view(state, x, y):
    if state.state == "explore":
        string = explore_view(state, x, y)
    elif state.state == "battle":
        string = battle_view(state, x, y)
    elif state.state == "weapon_menu":
        string = weapon_menu_view(state, x, y)
    elif state.state == 'armor_menu':
        string = armor_menu_view(state, x, y)
    elif state.state == "spell_menu":
        string = spell_menu_view(state, x, y)
    elif state.state == "game-over":
        string = game_over_view(state, x, y)
    elif state.state == 'loot_menu':
        string = loot_view(state, x, y)
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
    player = Player(100.00, name, 100, {'x': 2, 'y': 1}, _map[0])
    player.weapon = get_weapon('none')
    player.inventory['weapons'].append(get_weapon('none'))
    player.inventory['weapons'].append(get_weapon('Broken Dagger'))
    player.armor = get_armor('Leather')
    player.inventory['armors'].append(get_armor('none'))
    player.inventory['armors'].append(get_armor('Leather'))

    run(Game(player, _map, "explore"), update, view)


if __name__ == "__main__":
    main()
