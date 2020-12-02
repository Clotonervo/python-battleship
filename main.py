# import packages for program
import copy, random
import sys
import numpy as np
import math


# class to contain all of the battleship game
class BattleshipGame:
    # function to print the board

    def __init__(self):
        self.ships = {"Aircraft Carrier": 5,
                 "Battleship": 4,
                 "Submarine": 3,
                 "Destroyer": 3,
                 "Patrol Boat": 2}
        self.sunk_ships = []
        self.original_board = None;

    def print_board(self, s, board):
        # see if computer or user turn
        player = "Computer"
        if s == "u":
            player = "User"
        print("The " + player + "'s board look like this: \n")
        # print the horiz numbers
        print(" ", end=' ')
        for i in range(10):
            print("  " + str(i + 1) + "  ", end=' ')
        print("\n")
        for i in range(10):
            # print the vertical line number
            if i != 9:
                print(str(i + 1) + "  ", end=' ')
            else:
                print(str(i + 1) + " ", end=' ')
            # print the board values
            for j in range(10):
                if board[i][j] == -1:
                    print(' ', end=' ')
                elif s == "u":
                    print(board[i][j], end=' ')
                elif s == "c":
                    if board[i][j] == "*" or board[i][j] == "$":
                        print(board[i][j], end=' ')
                    else:
                        print(" ", end=' ')
                if j != 9:
                    print(" | ", end=' ')
            print()
            # print a horizontal line at end of rows
            if i != 9:
                print("   ----------------------------------------------------------")
            else:
                print()

                # function to let the user place the ships

    def user_place_ships(self, board, ships):
        """
        lets the user place ships and also check if they are valid positions
        """
        for ship in list(ships.keys()):
            # get coords and validate position
            valid = False
            while (not valid):
                self.print_board("u", board)
                print("Placing a/an " + ship)
                x, y = self.get_coor()
                ori = self.v_or_h()
                valid = self.validate(board, ships[ship], x, y, ori)
                if not valid:
                    print("Cannot place a ship there.\nPlease take a look at the board and try again.")
                    input("Press enter to continue")
            # place the ship
            board = self.place_ship(board, ships[ship], ship[0], ori, x, y)
            self.print_board("u", board)
        input("Done placing user ships. Press enter to continue")
        return board

    # place ships
    def computer_place_ships(self, board, ships):
        """
        computer will user random to generate ship places
        """
        for ship in list(ships.keys()):
            # genreate random coordinates and validate the postion
            valid = False
            while (not valid):
                # use randint from import random
                x = random.randint(1, 10) - 1
                y = random.randint(1, 10) - 1
                o = random.randint(0, 1)
                # vertical or horiz
                if o == 0:
                    ori = "v"
                else:
                    ori = "h"
                valid = self.validate(board, ships[ship], x, y, ori)
            # place the ship
            print("Computer placing a/an " + ship)
            board = self.place_ship(board, ships[ship], ship[0], ori, x, y)
        return board

    # let the user place a ship
    def place_ship(self, board, ship, s, ori, x, y):
        """
        accepts board, ship size, and position, places ship, it should already be verified by user_place_ships function
        """
        # orient ships
        if ori == "v":
            for i in range(ship):
                board[x + i][y] = s
        elif ori == "h":
            for i in range(ship):
                board[x][y + i] = s
        return board

    # check if the ship will actually fit, bool
    def validate(self, board, ship, x, y, ori):
        """
        check if ship will fit, based on ship size, board, orientation, and coordinates
        """
        if ori == "v" and x + ship > 10:
            return False
        elif ori == "h" and y + ship > 10:
            return False
        else:
            if ori == "v":
                for i in range(ship):
                    if board[x + i][y] != -1:
                        return False
            elif ori == "h":
                for i in range(ship):
                    if board[x][y + i] != -1:
                        return False
        return True

    # see if ship is horiz or vert
    def v_or_h(self):
        # get ship orientation from user
        while (True):
            user_input = input("vertical or horizontal (v,h) ? ")
            if user_input == "v" or user_input == "h":
                return user_input
            else:
                print("Invalid input. Please only enter v or h")


    def get_coor(self):
        """
        user will enter coordinates (row and column) for the ship to go
        """
        while (True):
            user_input = input("Please enter coordinates (row,col) ? ")
            try:
                # see that user entered 2 values seprated by comma
                coor = user_input.split(",")
                if len(coor) != 2:
                    raise Exception("Invalid entry, too few/many coordinates.");
                # check that 2 values are integers
                coor[0] = int(coor[0]) - 1
                coor[1] = int(coor[1]) - 1
                # check that values of integers are between 1 and 10 for both coordinates
                if coor[0] > 9 or coor[0] < 0 or coor[1] > 9 or coor[1] < 0:
                    raise Exception("Invalid entry. Please use values between 1 to 10 only.")
                # if everything is ok, return coordinates
                return coor
            # if the user enters something different
            except ValueError:
                print("Invalid entry. Please enter only numeric values for coordinates")
            except Exception as e:
                print(e)

    # see what move does
    def make_move(self, board, x, y):
        """
        make the move on the board and return the board, modified
        """
        if board[x][y] == -1:
            return "miss"
        elif board[x][y] == '*' or board[x][y] == '$':
            return "try again"
        else:
            return "hit"


    def user_move(self, board):
        """
        keep getting coordinates from the user and check if its a hit miss or sink
        """
        while (True):
            x, y = self.get_coor()
            res = self.make_move(board, x, y)
            if res == "hit":
                print("Hit at " + str(x + 1) + "," + str(y + 1))
                self.check_sink(board, x, y)
                board[x][y] = '$'
                if self.check_win(board):
                    return "WIN"
            elif res == "miss":
                print("Sorry, " + str(x + 1) + "," + str(y + 1) + " is a miss.")
                board[x][y] = "*"
            elif res == "try again":
                print("Sorry, that coordinate was already hit. Please try again")
            if res != "try again":
                return board


    def computer_move(self, board):
        """
        generate random coorindates for the computer to try using random
        same as user_move function, check for hit, sink, miss
        """
        while (True):
            x = random.randint(1, 10) - 1
            y = random.randint(1, 10) - 1
            res = self.make_move(board, x, y)
            if res == "hit":
                print("Hit at " + str(x + 1) + "," + str(y + 1))
                self.check_sink(board, x, y)
                board[x][y] = '$'
                if self.check_win(board):
                    return "WIN"
            elif res == "miss":
                print("Sorry, " + str(x + 1) + "," + str(y + 1) + " is a miss.")
                board[x][y] = "*"
            if res != "try again":
                return board

    def count_hits(self, window):
        hits = 0
        for i in window:
            if i == -2:
                hits += 1
        return hits


    #This function will define the probabilities that the ships are in any given square
    def define_probabilities(self, computer_view):
        probabilities = np.zeros((10, 10))
        ships = self.ships
        print(self.sunk_ships)
        #For each ship not sunk, check and see if there is a window, and add 1 to each place that its possible
        # for that ship to be, both vertial and horizontal
        # for example, if ship length = 3, then no windows of 2 should be included in those probabilities
        for x in range(0, len(probabilities)):
            for y in range(0, len(probabilities[0])):
                probabilities[x][y] = computer_view[x][y]

        for ship in ships:
            if ship in self.sunk_ships:
                continue
            ship_length = self.ships.get(ship)
            # get horizontal windows
            for x in range(0, len(probabilities)):
                for y in range(0, len(probabilities[0]) - ship_length + 1):
                    window = probabilities[x][y: y + ship_length]
                    if -1 in window:
                        continue
                    elif -3 in window:
                        continue
                    elif -2 in window:
                        hits = self.count_hits(window)
                        for i in range(0,len(window)):
                            if window[i] != -2:
                                window[i] += math.pow(10, hits)
                    else:
                        window += 1
            # get vertical windows
            for x in range(0, len(probabilities) - ship_length + 1):
                for y in range(0, len(probabilities[0])):
                    window = probabilities[x: x + ship_length, y]
                    if -1 in window:
                        continue
                    elif -3 in window:
                        continue
                    elif -2 in window:
                        hits = self.count_hits(window)
                        for i in range(0,len(window)):
                            if window[i] != -2:
                                window[i] += math.pow(10, hits)
                    else:
                        window += 1

        for x in range(0, len(probabilities)):
            for y in range(0, len(probabilities[0])):
                if computer_view[x][y] == -1:
                    probabilities[x][y] = -1
                elif computer_view[x][y] == -2:
                    probabilities[x][y] = -2
                elif computer_view[x][y] == -3:
                    probabilities[x][y] = -3

        print(probabilities)
        return probabilities

    # Here is the AI functionality
    def ai_move(self, computer_view, board):
        probabilities = self.define_probabilities(computer_view)
        max = 0
        for x in range(0, len(probabilities)):
            for y in range(0, len(probabilities[0])):
                if probabilities[x][y] > max:
                    max = probabilities[x][y]
                    row = x
                    col = y

        return self.ai_move_result(row, col, computer_view, board)

    def mark_ship_as_sunk(self, row, col, computer_view):
        ship_marking = self.original_board[row][col]
        # go through and mark all instances of that ship to -3 for sinked on the computer view board
        for x in range(0, len(computer_view)):
            for y in range(0, len(computer_view[0])):
                if self.original_board[x][y] == ship_marking:
                    computer_view[x][y] = -3

    #AI makes move, and here is what happens
    def ai_move_result(self, row, col, computer_view, board):
        res = self.make_move(board, row, col)
        if res == "hit":
            print("Hit at " + str(row + 1) + "," + str(col + 1))
            sinked = self.check_sink(board, row, col)
            computer_view[row][col] = -2
            if sinked != "X":
                self.sunk_ships.append(sinked)
                self.mark_ship_as_sunk(row, col, computer_view)
            board[row][col] = '$'
            if self.check_win(board):
                return "WIN"
        elif res == "miss":
            print("Sorry, " + str(row + 1) + "," + str(col + 1) + " is a miss.")
            board[row][col] = "*"
            computer_view[row][col] = -1
        if res != "try again":
            return board

    def check_sink(self, board, x, y):
        """
        figure out which ship is hit, then see how many points still exist in the ship, then see if sunk.
        the ship is sunk if there are no more points left
        """
        if board[x][y] == "A":
            ship = "Aircraft Carrier"
        elif board[x][y] == "B":
            ship = "Battleship"
        elif board[x][y] == "S":
            ship = "Submarine"
        elif board[x][y] == "D":
            ship = "Destroyer"
        elif board[x][y] == "P":
            ship = "Patrol Boat"
        # mark cell as hit and check if sunk
        board[-1][ship] -= 1
        if board[-1][ship] == 0:
            print(ship + " Sunk")
            return ship
        return "X"

    def check_win(self, board):
        """
        once all ships are sunk, then someone wins, end game
        if anything is not a hit, then return false
        """
        for i in range(10):
            for j in range(10):
                if board[i][j] != -1 and board[i][j] != '*' and board[i][j] != '$':
                    return False
        return True

    # function called to start program
    def main(self, ai):
        # types of ships
        # setup blank 10x10 board
        board = []
        for i in range(10):
            board_row = []
            for j in range(10):
                board_row.append(-1)
            board.append(board_row)
        # setup user and computer boards
        user_board = copy.deepcopy(board)
        comp_board = copy.deepcopy(board)
        # add ships in array
        user_board.append(copy.deepcopy(self.ships))
        comp_board.append(copy.deepcopy(self.ships))
        # ship placement
        user_board = self.computer_place_ships(user_board, self.ships)
        comp_board = self.computer_place_ships(comp_board, self.ships)
        self.original_board = copy.deepcopy(user_board)
        computer_view = np.zeros((10,10));

        # game main loop
        #owen
        while (1):
            # user move
            # self.print_board("c", comp_board)
            comp_board = self.user_move(comp_board)
            # check if user won
            if comp_board == "WIN":
                print("User WON! :)")
                quit()
            # display current computer board
            self.print_board("c", comp_board)
            # computer move
            # print(ai)
            # if ai == "ai":
            user_board = self.ai_move(computer_view, user_board)
            # else:
            #     user_board = self.computer_move(user_board)
            # check if computer move
            if user_board == "WIN":
                print("Computer WON! :(")
                quit()
            self.print_board("u", user_board)

            # display user board


root = BattleshipGame()
root.main(sys.argv[1])
