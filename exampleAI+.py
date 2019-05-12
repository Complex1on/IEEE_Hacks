from colorfight import Colorfight
import time
import random
import math
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS


def lowestDist():
    # find adjacent cells
    adjcells = []
    for cell in game.me.cells.values():
        for pos in cell.position.get_surrounding_cardinals():
            c = game.game_map[pos]
            if c.owner != game.uid and c not in adjcells:
                adjcells.append(c)
    # [c.position, dist, c.attack_cost]

    potential = []
    for cell2 in adjcells:
        dist = math.sqrt((home.position.x - cell2.position.x) ** 2 +
                         (home.position.y - cell2.position.y)**2)
        potential.append([cell2, dist])
    potential.sort(key=lambda x: x[1])

    for attackcell in potential:
        if attackcell[0].attack_cost < me.energy:
            cmd_list.append(game.attack(
                attackcell[0].position, attackcell[0].attack_cost))
            # print("We are attacking ({}, {}) with {} energy".format(
            #   attackcell[0].position.x, attackcell[0].position.y, attackcell[0].attack_cost))
            game.me.energy -= attackcell[0].attack_cost


game = Colorfight()


game.connect(room='Hi')


if game.register(username='ExampleAI' + str(random.randint(1, 100)),
                 password=str(int(time.time())), join_key="testing123"):
    # This is the game loop
    numEn = 0
    numGold = 0
    numFort = 0

    while True:

        cmd_list = []

        my_attack_list = []

        game.update_turn()

        if game.me == None:
            continue

        me = game.me
        home = None
        for cell in game.me.cells.values():
            c = game.game_map[cell.position]
            if c.is_home:
                home = c

        if (len(me.cells) < 250):
            lowestDist()
        for cell in game.me.cells.values():

            # if cell.building.can_upgrade and \
            #     (cell.building.is_home or cell.building.level < me.tech_level) and \
            #     cell.building.upgrade_gold < me.gold and \
            #         cell.building.upgrade_energy < me.energy:
            #     cmd_list.append(game.upgrade(cell.position))
            #     print("We upgraded ({}, {})".format(
            #         cell.position.x, cell.position.y))
            #     me.gold -= cell.building.upgrade_gold
            #     me.energy -= cell.building.upgrade_energy

            # Build a random building if we have enough gold
            print("ENERGY IS ")
            print(me.energy)
            print("NUM CELLS IS")
            print(len(me.cells))
            if (len(me.cells) < 250):
                if cell.owner == me.uid and cell.building.is_empty and me.gold > 6000:
                    building = BLD_FORTRESS
                    cmd_list.append(game.build(cell.position, building))
                    print("We build {} on ({}, {})".format(
                        building, cell.position.x, cell.position.y))
                    me.gold -= 100
                if cell.owner == me.uid and cell.building.is_empty and me.energy < 75:
                    building = BLD_ENERGY_WELL
                    cmd_list.append(game.build(cell.position, building))
                    print("We build {} on ({}, {})".format(
                        building, cell.position.x, cell.position.y))
                    me.gold -= 100
                if cell.owner == me.uid and cell.building.is_empty and me.energy >= 75:
                    building = BLD_GOLD_MINE
                    cmd_list.append(game.build(cell.position, building))
                    print("We build {} on ({}, {})".format(
                        building, cell.position.x, cell.position.y))
                    me.gold -= 100
            if(me.gold > 1000 and me.energy > 1000):
                cmd_list.append(game.upgrade(home.pos))

            if cell.building.can_upgrade < me.tech_level and \
                    cell.building.upgrade_gold < me.gold and cell.building.upgrade_energy < me.energy:
                cmd_list.append(game.upgrade(cell.position))
                me.gold -= cell.building.upgrade_gold
                me.energy -= cell.building.upgrade_energy

        # Send the command list to the server
        result = game.send_cmd(cmd_list)
        print(result)
