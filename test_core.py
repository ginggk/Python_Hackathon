from core import *


def test_load_armor():
    none = {'name': "none", 'defense': 0}
    leather = {'name': "Leather", 'defense': 1}
    armors = [none, leather]

    assert load_armor() == [none, leather]


def test_get_armor():
    armors = load_armor()
    name = "Leather"

    assert get_armor(name) == {'name': "Leather", 'defense': 1}


def test_load_weapons():
    none = {'name': 'none', 'multiplier': 1, 'sharpness': 0}
    broken_dagger = {'name': 'Broken Dagger', 'multiplier': 1.2}
    weapons = [none, broken_dagger]

    assert load_weapons() == [none, broken_dagger]


def test_get_weapon():
    weapons = load_weapons()
    name = "Broken Dagger"

    assert get_weapon(name) == {'name': 'Broken Dagger', 'multiplier': 1.2}


def test_attack():
    class Player:
        def __init__(self, base_attack, weapon):
            self.base_attack = 5
            self.weapon = {"multiplier": 1}

    class Enemy:
        def __init__(self, health, armor):
            self.health = 100
            self.armor = {"defense": 1}

    player = Player(5, {"multiplier": 1})
    enemy = Enemy(100, {"defense": 1})

    assert attack(player, enemy) == player


def test_cast_spell():
    class Player:
        def __init__(self, base_attack, weapon, spell, magic):
            self.base_attack = 5
            self.weapon = {"multiplier": 1}
            self.spell = "Firepuff"
            self.magic = 50

    class Enemy:
        def __init__(self, health, armor):
            self.health = 100
            self.armor = {"defense": 1}

    player = Player(5, {"multiplier": 1}, "Firepuff", 50)
    enemy = Enemy(100, {"defense": 1})

    assert cast_spell(player, enemy) == player


def test_equip_weapon():
    class Player:
        def __init__(self, base_attack, weapon, spell, magic, inventory):
            self.base_attack = 5
            self.weapon = {'name': 'dagger', "multiplier": 1}
            self.inventory = {
                "weapons": [{
                    'name': 'dagger',
                    "multiplier": 1
                }, {
                    'name': 'knife',
                    "multiplier": 2
                }]
            }

            self.spell = "Firepuff"
            self.magic = 50

    class Enemy:
        def __init__(self, health, armor):
            self.health = 100
            self.armor = {"defense": 1}

    player = Player(5, {
        'name': 'dagger',
        "multiplier": 1
    }, 'Firepuff', 50, {
        "weapons": [{
            'name': 'dagger',
            "multiplier": 1
        }, {
            'name': 'knife',
            "multiplier": 2
        }]
    })
    index = 1

    assert equip_weapon(player, index) == player


def test_equip_armor():
    class Player:
        def __init__(self, base_attack, weapon, spell, magic, inventory):
            self.base_attack = 5
            self.weapon = {'name': 'dagger', "multiplier": 1}
            self.inventory = {
                "armors": [{
                    'name': 'chestplate',
                    "defense": 3
                }, {
                    'name': 'leather',
                    "defense": 1
                }]
            }

            self.spell = "Firepuff"
            self.magic = 50

    class Enemy:
        def __init__(self, health, armor):
            self.health = 100
            self.armor = {"defense": 1}

    player = Player(5, {
        'name': 'dagger',
        "multiplier": 1
    }, 'Firepuff', 50, {
        "armors": [{
            'name': 'chestplate',
            "defense": 3
        }, {
            'name': 'leather',
            "defense": 1
        }]
    })
    index = 1
    assert equip_armor(player, index) == player


# def test_load_map():
