"""
Tic-Tac-Toe with Minimax AI
Author: Nitishwar Vasantha Kumar
Date: October 28, 2025

Tic-Tac-Toe game where human plays against computer using Minimax algorithm.
"""

class Board:
    """Manages the 3x3 game board"""

    def __init__(self):
        # Initialize empty 3x3 board
        self.c = [[" " for _ in range(3)] for _ in range(3)]

    def printBoard(self):
        """Display the board with row and column indices"""
        print("\n   0   1   2")
        for i in range(3):
            print(f"{i}  " + " | ".join(self.c[i]))
            if i < 2:
                print("  -----------")
        print()


class Game:
    """Handles Tic-Tac-Toe logic and Minimax AI"""

    def __init__(self):
        self.board = Board()
        self.turn = 'X'  # Human always starts

    def switchPlayer(self):
        """Switch turn between X and O"""
        self.turn = 'O' if self.turn == 'X' else 'X'

    def validateEntry(self, row, col):
        """Return True if move is valid (in range and empty)"""
        return 0 <= row < 3 and 0 <= col < 3 and self.board.c[row][col] == " "

    def checkFull(self):
        """Return True if board is full"""
        return all(cell != " " for row in self.board.c for cell in row)

    def checkWin(self):
        """Return True if current player has won"""
        b = self.board.c
        t = self.turn
        # Check rows and columns
        for i in range(3):
            if all(b[i][j] == t for j in range(3)) or all(b[j][i] == t for j in range(3)):
                return True
        # Check diagonals
        if all(b[i][i] == t for i in range(3)) or all(b[i][2 - i] == t for i in range(3)):
            return True
        return False

    def checkEnd(self):
        """Return True if game is over (win or draw)"""
        return self.checkWin() or self.checkFull()

    def checkWinState(self, board_state, player):
        """Check if a specific player has won on a given board state"""
        # Rows
        for row in board_state:
            if all(cell == player for cell in row):
                return True
        # Columns
        for col in range(3):
            if all(board_state[r][col] == player for r in range(3)):
                return True
        # Diagonals
        if all(board_state[i][i] == player for i in range(3)):
            return True
        if all(board_state[i][2 - i] == player for i in range(3)):
            return True
        return False

    def minimax(self, board_state, is_maximizing):
        """
        Minimax algorithm for optimal computer move.
        Args:
            board_state (list of list): Current 3x3 board as list of lists.
            is_maximizing (bool): True if computer's turn (O), False if human's turn (X)
        Returns:
            int: +1 if O wins, -1 if X wins, 0 for draw
        """
        if self.checkWinState(board_state, 'O'):
            return 1
        elif self.checkWinState(board_state, 'X'):
            return -1
        elif all(cell != ' ' for row in board_state for cell in row):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board_state[i][j] == ' ':
                        board_state[i][j] = 'O'
                        score = self.minimax(board_state, False)
                        board_state[i][j] = ' '
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board_state[i][j] == ' ':
                        board_state[i][j] = 'X'
                        score = self.minimax(board_state, True)
                        board_state[i][j] = ' '
                        best_score = min(best_score, score)
            return best_score

    def getComputerMove(self):
        """Determine the optimal move for computer (O) using Minimax"""
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board.c[i][j] == ' ':
                    self.board.c[i][j] = 'O'
                    score = self.minimax(self.board.c, False)
                    self.board.c[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        print("Computer has calculated its best possible move.")
        return best_move

    def playGame(self):
        """Main game loop"""
        print("Welcome to Tic-Tac-Toe!")
        print("You are X, Computer is O\n")

        while True:
            self.board.printBoard()

            if self.turn == 'X':
                print(f"\n{self.turn}'s turn.")
                print(f"Where do you want your {self.turn} placed?")
                print("Please enter row number and column number separated by a comma.")

                move = input().strip()
                try:
                    row_str, col_str = move.split(",")
                    row, col = int(row_str), int(col_str)
                    print(f"You have entered row #{row}\nand column #{col}")
                except (ValueError, IndexError):
                    print("Invalid entry: try again.")
                    print("Row & column numbers must be either 0, 1, or 2.")
                    continue

                if not self.validateEntry(row, col):
                    if not (0 <= row < 3 and 0 <= col < 3):
                        print("Invalid entry: try again.")
                        print("Row & column numbers must be either 0, 1, or 2.")
                    else:
                        print("That cell is already taken.")
                        print("Please make another selection.")
                    continue

                self.board.c[row][col] = 'X'

            else:
                # Computer's turn
                print(f"\n{self.turn}'s turn (Computer analyzing the board...)")
                move = self.getComputerMove()
                if move:
                    row, col = move
                    self.board.c[row][col] = 'O'
                    print(f"Computer placed O at row {row}, column {col}")

            # Check if game ended
            if self.checkEnd():
                self.board.printBoard()
                if self.checkWin():
                    if self.turn == 'X':
                        print("Congratulations! You won!")
                    else:
                        print("Computer wins!")
                else:
                    print("DRAW! Nobody wins!")
                break

            # Switch turn
            self.switchPlayer()

        # Ask for replay
        again = input("\nAnother game? Enter Y or y for yes: ").strip().lower()
        if again == 'y':
            self.board = Board()
            self.turn = 'X'
            self.playGame()
        else:
            print("Thank you for playing!")


def main():
    game = Game()
    game.playGame()


if __name__ == "__main__":
    main()
