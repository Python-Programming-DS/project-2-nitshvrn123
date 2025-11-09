"""
File Name : NV_Project2_PartA.py
Tic-Tac-Toe
Author: Nitishwar Vasantha Kumar
Date: October 27, 2025

Two-player Tic-Tac-Toe game using classes and objects.
"""

class Board:
    """ This manages the 3x3 game board"""

    def __init__(self):
        # create empty 3x3 board
        self.c = [[" " for _ in range(3)] for _ in range(3)]

    def printBoard(self):
        """Display board with row/column indices"""
        print("\n   0   1   2")
        for i in range(3):
            print(f"{i}  " + " | ".join(self.c[i]))
            if i < 2:
                print("  -----------")
        print()


class Game:
    """Handles game logic and flow"""

    def __init__(self):
        # initialize game with empty board, X starts
        self.board = Board()
        self.turn = 'X'

    def switchPlayer(self):
        """Switch between X and O"""
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

    def validateEntry(self, row, col):
        """Check if move is valid (in range and cell empty)"""
        if 0 <= row < 3 and 0 <= col < 3:
            if self.board.c[row][col] == " ":
                return True
        return False

    def checkFull(self):
        """Check if all cells are filled"""
        return all(cell != " " for row in self.board.c for cell in row)

    def checkWin(self):
        """Check if current player won"""
        b = self.board.c
        t = self.turn

        # check rows
        for row in b:
            if all(cell == t for cell in row):
                return True

        # check columns
        for col in range(3):
            if all(b[r][col] == t for r in range(3)):
                return True

        # check diagonals
        if all(b[i][i] == t for i in range(3)):
            return True
        if all(b[i][2 - i] == t for i in range(3)):
            return True

        return False

    def checkEnd(self):
        """Game ends if win or board full"""
        return self.checkWin() or self.checkFull()

    def playGame(self):
        """Main game loop"""
        print("Welcome to Tic-Tac-Toe!")

        while True:
            self.board.printBoard()
            print(f"\n{self.turn}'s turn.")
            print(f"Where do you want your {self.turn} placed?")
            print("Please enter row number and column number separated by a comma.")

            # get player input
            move = input().strip()
            try:
                row_str, col_str = move.split(",")
                row, col = int(row_str), int(col_str)
                print(f"You have entered row #{row}\nand column #{col}")
            except (ValueError, IndexError):
                print("Invalid entry: try again.")
                print("Row & column numbers must be either 0, 1, or 2.")
                continue

            # validate move
            if not self.validateEntry(row, col):
                if not (0 <= row < 3 and 0 <= col < 3):
                    print("Invalid entry: try again.")
                    print("Row & column numbers must be either 0, 1, or 2.")
                else:
                    print("That cell is already taken.")
                    print("Please make another selection.")
                continue

            # make move
            self.board.c[row][col] = self.turn

            # check if game ended
            if self.checkWin():
                self.board.printBoard()
                print(f"{self.turn} IS THE WINNER!!!")
                break
            elif self.checkFull():
                self.board.printBoard()
                print("DRAW! NOBODY WINS!")
                break

            # switch to other player
            self.switchPlayer()

        # ask to play again
        again = input("\nAnother game? Enter Y or y for yes.\n").strip().lower()
        if again == 'y':
            self.board = Board()
            self.turn = 'X'
            self.playGame()
        else:
            print("Thank you for playing!")


def main():
    """Start the game"""
    game = Game()
    game.playGame()


if __name__ == "__main__":
    main()
