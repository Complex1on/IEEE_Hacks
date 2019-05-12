from colorfight import Colorfight
import time
import random
import math
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

# Create a Colorfight Instance. This will be the object that you interact
# with.
game = Colorfight()

# Connect to the server. This will connect to the public room. If you want to
# join other rooms, you need to change the argument
game.connect(room='Hi')

# game.register should return True if succeed.
# As no duplicate usernames are allowed, a random integer string is appended
# to the example username. You don't need to do this, change the username
# to your ID.
# You need to set a password. For the example AI, the current time is used
# as the password. You should change it to something that will not change
# between runs so you can continue the game if disconnected.


def lowestDist():
    # find adjacent cells
    adjcells = []
    for cell in game.me.cells.values():
        for pos in cell.position.get_surrounding_cardinals():
            c = game.game_map[pos]
            dist = math.sqrt((home.position.x - c.position.x) ** 2 +
                             (home.position.y - c.position.y)**2)
            if c.owner != game.uid and c not in adjcells and c.attack_cost < me.energy:
                adjcells.append([c.position, dist, c.attack_cost])

    adjcells.sort(key=lambda x: x[1])

    for attackcell in adjcells:
        if attackcell[2] < me.energy:
            cmd_list.append(game.attack(attackcell[0], attackcell[2]))
            print("We are attacking ({}, {}) with {} energy".format(
                attackcell[0].x, attackcell[0].y, attackcell[2]))
            game.me.energy -= attackcell[2]


def lowestDistBuilding():
    lst = []
    for cell in game.me.cells.values():
        c = game.game_map[cell.position]
        dist = math.sqrt((home.position.x - c.position.x) ** 2 +
                         (home.position.y - c.position.y)**2)
        if c.owner == game.uid and c not in lst and c.building.is_empty == True:
            lst.append([c.position, dist])
    lst.sort(key=lambda x: x[1])
    return lst[0]


def findHome(game):
    for cell in game.me.cells.values():
        c = game.game_map[cell.position]
        if c.is_home:
            return c


if game.register(username='ItGonnaBreak' + str(random.randint(1, 100)),
                 password=str(int(time.time())), join_key="testing123"):
    # This is the game loop
    numGold = 0
    numEn = 0
    game.update_turn()

    while True:
        game.update_turn()
        me = game.me
        home = None
        for cell in game.me.cells.values():
            c = game.game_map[cell.position]
            if c.is_home:
                home = c

        cmd_list = []
        my_attack_list = []

        lowestDist()
        # print(attackcell)

        if len(me.cells) > 2 and me.gold >= 100:
            building = random.choice([BLD_GOLD_MINE, BLD_ENERGY_WELL])
            build = lowestDistBuilding()
            print("We build {} on ({}, {})".format(
                building, build[0].x, build[0].y))
            cmd_list.append(game.build(build[0], building))
            me.gold -= 100

        # if numGold < 10 and len(me.cells) > 2:
        #     building = BLD_GOLD_MINE
        #     build = lowestDistBuilding()
        #     print("We build {} on ({}, {})".format(
        #         building, build[0].x, build[0].y))
        #     cmd_list.append(game.build(build[0], building))
        #     me.gold -= 100
        #     numGold += 1
        #     print(numGold)
        # elif numGold > 10 and len(me.cells) > 2:
        #     building = BLD_ENERGY_WELL
        #     build = lowestDistBuilding()
        #     print("We build {} on ({}, {})".format(
        #         building, build[0].x, build[0].y))
        #     cmd_list.append(game.build(build[0], building))
        #     me.gold -= 100
        #     numEn += 1

        # Send the command list to the server
        result = game.send_cmd(cmd_list)
        print(result)
