# begin
from random import randint
import numpy as np


class BattleShipGame():
    # create 3d matrix
    userArr = np.zeros((8, 8))
    aiArr = np.zeros((8, 8))
    ship_lengths = [1, 2, 3, 4]

    # function to place AI ships
    def placeShips(self):
        for i in ship_lengths:
            for j in range(0, i):
                previous_point = []
                while (True):
                    a = [randint(0, len(aiArr) - 1), randint(0, len(aiArr) - 1)]
                    if j == 0:
                        if aiArr[a[0], a[1]] == 0:
                            aiArr[a[0], a[1]] = 1
                            break;
                    elif aiArr[a[0], a[1]] == 0 and isNextTo(aiArr[a[0], a[1]], previous_point
                    aiArr[a[0], a[1]] == 1
                    previous_point =[a[0], a[1]]

                    # check if said point is next to another, if it is, place

    def isNextTo(self, point1, point2):
        if point1[0] + 1 == point2[0] or point1[0] - 1 == point2[0]:
            return True
        elif point1[1] + 1 == point2[1] or point1[1] - 1 == point2[1]:
            return True
        else:
            return False

    # function to let user choose coordinates of ship to hit

    # function to let user place ships

    # function to see if the user hits the ships

    # data structure to store ships and hits

    # function to see if ship is sunk

    # function to start game
