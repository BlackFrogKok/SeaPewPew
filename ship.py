from const import *


class Ship:
    def __init__(self, y, x, len_ship, orient):
        self.x = x
        self.y = y
        self.len_ship = len_ship
        self.ship_health = len_ship
        self.orient = orient
        self.value = 1
        self.height = len_ship if orient == shipOrientation.NORMAL else 1
        self.width = 1 if orient == shipOrientation.NORMAL else len_ship

    def damage(self):
        self.ship_health -= 1
        if self.ship_health == 0:
            return 1

'''    def change_orient(self):
        self.height = 1 if self.orient == shipOrientation.NORMAL else self.len_ship
        self.width = self.len_ship if self.orient == shipOrientation.NORMAL else 1'''
