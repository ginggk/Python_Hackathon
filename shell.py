from pybcca.tui_helper import run
from core import *
import os
import emoji


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


def remove_inventory_update(key, state):
    if key == 'w':
        state.state = 'remove_weapon'
    elif key == 'a':
        state.state = 'remove_armor'
    elif key == 's':
        state.state = 'remove_spell'
    return state


def remove_weapon_update(key, state):
    if key == '1':
        remove_item(state.player, 1, 'weapons')
        state.state = "loot_menu"
    elif key == '2':
        remove_item(state.player, 2, 'weapons')
        state.state = "loot_menu"
    elif key == '3':
        remove_item(state.player, 3, 'weapons')
        state.state = "loot_menu"
    elif key == '4':
        remove_item(state.player, 4, 'weapons')
        state.state = "loot_menu"
    elif key == '5':
        remove_item(state.player, 5, 'weapons')
        state.state = "loot_menu"
    elif key == '6':
        remove_item(state.player, 6, 'weapons')
        state.state = "loot_menu"
    elif key == '7':
        remove_item(state.player, 7, 'weapons')
        state.state = "loot_menu"
    elif key == '8':
        remove_item(state.player, 8, 'weapons')
        state.state = "loot_menu"
    elif key == '9':
        remove_item(state.player, 9, 'weapons')
        state.state = "loot_menu"
    return state


def remove_armor_update(key, state):
    if key == '1':
        remove_item(state.player, 1, 'armors')
    elif key == '2':
        remove_item(state.player, 2, 'armors')
    elif key == '3':
        remove_item(state.player, 3, 'armors')
    elif key == '4':
        remove_item(state.player, 4, 'armors')
    elif key == '5':
        remove_item(state.player, 5, 'armors')
    elif key == '6':
        remove_item(state.player, 6, 'armors')
    elif key == '7':
        remove_item(state.player, 7, 'armors')
    elif key == '8':
        remove_item(state.player, 8, 'armors')
    elif key == '9':
        remove_item(state.player, 9, 'armors')
    elif key == 'd':
        state.state = 'loot_menu'
    return state


def remove_spell_update(key, state):
    if key == '1':
        remove_item(state.player, 1, 'spell-book')
        state.state = "loot_menu"
    elif key == '2':
        remove_item(state.player, 2, 'spell-book')
        state.state = "loot_menu"
    elif key == '3':
        remove_item(state.player, 3, 'spell-book')
        state.state = "loot_menu"
    elif key == '4':
        remove_item(state.player, 4, 'spell-book')
        state.state = "loot_menu"
    elif key == '5':
        remove_item(state.player, 5, 'spell-book')
        state.state = "loot_menu"
    elif key == '6':
        remove_item(state.player, 6, 'spell-book')
        state.state = "loot_menu"
    elif key == '7':
        remove_item(state.player, 7, 'spell-book')
        state.state = "loot_menu"
    elif key == '8':
        remove_item(state.player, 8, 'spell-book')
        state.state = "loot_menu"
    elif key == '9':
        remove_item(state.player, 9, 'spell-book')
        state.state = "loot_menu"
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
    elif state.state == 'remove_inventory_menu':
        state = remove_inventory_update(key, state)
    elif state.state == 'remove_weapon':
        state = remove_weapon_update(key, state)
    elif state.state == 'remove_armor':
        state = remove_armor_update(key, state)
    elif state.state == 'remove_spell':
        state = remove_spell_update(key, state)

    return state


def explore_view(state, x, y):
    string = f'Use the Arrow keys to move\nPlayer: {state.player.name}\n\n\t'
    for row in state.player.room.build:
        for cell in row:
            if cell == 0:
                string += "  "
            elif cell == 1:
                string += emoji.emojize(":full_moon:")
            elif cell == 2:
                string += emoji.emojize(":musical_keyboard:")
            elif cell == 3:
                string += emoji.emojize(":door:")
            elif cell == 4:
                string += emoji.emojize(":skull:")
            elif cell == 5:
                string += emoji.emojize(":door:")
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


def weapon_remove_view(state, x, y):
    string = "Choose a weapon to remove\n"
    counter = 1

    for weapon in state.player.inventory['weapons'][1:]:
        new_str = f'{counter}: {weapon["name"]}\n'
        counter += 1
        string += new_str
    return string


def armor_remove_view(state, x, y):
    string = "Choose an Armor to remove\n"
    counter = 1
    controls = "\n[D] Done"

    for armor in state.player.inventory['armors'][1:]:
        new_str = f'{counter}: {armor["name"]}\n'
        counter += 1
        string += new_str
    return string + controls


def spell_remove_view(state, x, y):
    string = "Choose a Spell to remove\n"
    counter = 1

    for spell in state.player.inventory['spell-book'][1:]:
        new_str = f'{counter}: {spell["name"]}\n'
        counter += 1
        string += new_str
    return string


def remove_inventory_view(state, x, y):
    string = "Choose A Category to Edit\n[W] Weapons\t [A] Armor\t [S] Spell-Book"
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
    spells = f"[4] Spell: {state.enemy.loot[3]['name']}\n"

    inv = f"\n\n\n{state.player.inventory['armors']}"

    controls = "\n\n\n[D] Done\t[S] Edit Inventory"

    return string + gold + weapon + armor + spells + controls


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
    elif state.state == "remove_inventory_menu":
        string = remove_inventory_view(state, x, y)
    elif state.state == 'remove_weapon':
        string = weapon_remove_view(state, x, y)
    elif state.state == 'remove_armor':
        string = armor_remove_view(state, x, y)
    elif state.state == 'remove_spell':
        string = spell_remove_view(state, x, y)
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

    run(Game(player, _map, "explore", 0), update, view)


if __name__ == "__main__":
    main()
