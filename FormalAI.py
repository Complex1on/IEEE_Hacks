from colorfight import Colorfight
import time
import random
import math
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS


class AI:
    def __init__(self, game, home, me):
        self.game = game
        self.home = home
        self.numGold = 0
        self.numEn = 0
        self.me = me

    def lowestDist(self):
        # find adjacent cells
        adjcells = []
        for cell in self.game.me.cells.values():
            for pos in cell.position.get_surrounding_cardinals():
                c = self.game.game_map[pos]
                dist = math.sqrt((self.home.position.x - c.position.x) ** 2 +
                                 (self.home.position.y - c.position.y)**2)
                if c.owner != self.game.uid and c not in adjcells:
                    adjcells.append([c.position, dist, c.attack_cost])

        adjcells.sort(key=lambda x: x[1])
        return adjcells[0]

    def lowestDistBuilding(self):
        lst = []
        for cell in self.game.me.cells.values():
            c = self.game.game_map[cell.position]
            dist = math.sqrt((self.home.position.x - c.position.x) ** 2 +
                             (self.home.position.y - c.position.y)**2)
            if c.owner == self.game.uid and c not in lst and c.building.is_empty == True:
                lst.append([c.position, dist])
        lst.sort(key=lambda x: x[1])
        return lst[0]

    def behave(self):
        self.game.update_turn()
        self.me = self.game.me
        cmd_list = []
        my_attack_list = []

        attackcell = self.lowestDist()
        # print(attackcell)
        cmd_list.append(self.game.attack(attackcell[0], attackcell[2]))
        print("We are attacking ({}, {}) with {} energy".format(
            attackcell[0].x, attackcell[0].y, attackcell[2]))
        self.game.me.energy -= attackcell[2]
        my_attack_list.append(attackcell[0])

        if self.numGold < 10 and len(self.me.cells) > 2:
            building = BLD_GOLD_MINE
            build = self.lowestDistBuilding()
            print("We build {} on ({}, {})".format(
                building, build[0].x, build[0].y))
            cmd_list.append(game.build(build[0], building))
            self.me.gold -= 100
            self.numGold += 1
            print(self.numGold)
        elif self.numGold > 10 and len(self.me.cells) > 2:
            building = BLD_ENERGY_WELL
            build = self.lowestDistBuilding()
            print("We build {} on ({}, {})".format(
                building, build[0].x, build[0].y))
            cmd_list.append(game.build(build[0], building))
            self.me.gold -= 100

        # Send the command list to the server
        result = game.send_cmd(cmd_list)
        print(result)

    def test(self):
        test = self.lowestDist()
        test2 = self.lowestDistBuilding()
        print(test)
        print(test2)


def findHome(game):
    for cell in game.me.cells.values():
        c = game.game_map[cell.position]
        if c.is_home:
            return c


if __name__ == "__main__":
    game = Colorfight()
    game.connect(room='Hi')
    print("STARTING PROGRAM")
    game.update_turn()

    if game.register(username='ItGonnaBreak4', password="testing", join_key="testing123"):
        game.update_turn()
        me = game.me
        home = findHome(game)

        myai = AI(game, home, me)

        while True:
            game.update_turn()
            print("working")
            myai.behave()
