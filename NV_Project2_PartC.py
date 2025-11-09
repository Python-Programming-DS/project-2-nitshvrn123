"""
Tic-Tac-Toe with Machine Learning AI (Part C)
Author: Nitishwar Vasantha Kumar
Date: October 29, 2025

Human plays X vs ML-based computer O using Random Forest trained on
'tictac_single.txt' intermediate board dataset (player O = -1).
"""

import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score


class Board:
    """Manages the 3x3 game board"""

    def __init__(self):
        # Create an empty 3x3 board
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
    """Handles the Tic-Tac-Toe logic and ML-based AI"""

    def __init__(self, model):
        self.board = Board()
        self.turn = 'X'
        self.model = model

    def switchPlayer(self):
        """Switch turns between X and O"""
        self.turn = 'O' if self.turn == 'X' else 'X'

    def validateEntry(self, row, col):
        """Check if a move is valid"""
        return 0 <= row < 3 and 0 <= col < 3 and self.board.c[row][col] == " "

    def checkFull(self):
        """Return True if the board is full"""
        return all(cell != " " for row in self.board.c for cell in row)

    def checkWin(self):
        """Check if current player has won"""
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

    def encodeBoard(self):
        """Convert board to numeric input for model (X=1, O=-1, empty=0)"""
        encoded = []
        for row in self.board.c:
            for cell in row:
                if cell == "X":
                    encoded.append(1)
                elif cell == "O":
                    encoded.append(-1)
                else:
                    encoded.append(0)
        return encoded

    def getComputerMove(self):
        """Use trained ML model to predict best move for O"""
        encoded = self.encodeBoard()
        move_index = self.model.predict([encoded])[0]
        row, col = divmod(move_index, 3)

        # Handle invalid prediction gracefully
        if not self.validateEntry(row, col):
            available = [(r, c) for r in range(3) for c in range(3) if self.board.c[r][c] == " "]
            row, col = random.choice(available)
            print("(ML predicted invalid move — choosing a random valid spot.)")
        return row, col

    def playGame(self):
        """Main game loop"""
        print("Welcome to Tic-Tac-Toe (Part C)")
        print("You are X, Computer is O (ML AI)\n")

        while True:
            self.board.printBoard()

            if self.turn == 'X':
                # Human player's turn
                print(f"{self.turn}'s turn.")
                try:
                    move = input("Enter your move as row,col (e.g., 1,2): ").strip()
                    row_str, col_str = move.split(",")
                    row, col = int(row_str), int(col_str)
                except (ValueError, IndexError):
                    print("Invalid input. Format: row,col (numbers 0–2). Try again.")
                    continue

                if not self.validateEntry(row, col):
                    print("Invalid move: cell taken or out of range.")
                    continue

                self.board.c[row][col] = 'X'

            else:
                # Computer's turn
                print(f"{self.turn}'s turn (Computer thinking...)")
                print("Computer chooses the optimal move.")
                row, col = self.getComputerMove()
                self.board.c[row][col] = 'O'
                print(f"Computer placed O at row {row}, column {col}")

            # Check for win or draw
            if self.checkWin():
                self.board.printBoard()
                if self.turn == 'X':
                    print("Congratulations! You win!")
                else:
                    print("Computer wins!")
                break
            elif self.checkFull():
                self.board.printBoard()
                print("DRAW! Nobody wins!")
                break

            # Switch turns
            self.switchPlayer()

        # Ask for replay
        again = input("\nAnother game? Enter Y or y for yes.\n").strip().lower()
        if again == 'y':
            self.board = Board()
            self.turn = 'X'
            self.playGame()
        else:
            print("Thank you for playing!")


def load_dataset(filename):
    """Load tictac dataset into X (board states) and y (best move)"""
    X, y = [], []
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 10:
                features = list(map(int, parts[:9]))
                label = int(parts[9])
                X.append(features)
                y.append(label)
    return X, y


def train_model(X, y):
    """Train and fine-tune a Random Forest model using GridSearchCV"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    param_grid = {
        "n_estimators": [50, 100, 150],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2]
    }

    grid = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid,
        scoring="accuracy",
        cv=3,
        n_jobs=-1,
        verbose=0
    )

    grid.fit(X_train, y_train)
    best_model = grid.best_estimator_

    # Evaluate model
    acc = accuracy_score(y_test, best_model.predict(X_test))
    print(f"Best parameters: {grid.best_params_}")
    print(f"Model trained successfully (Validation Accuracy: {acc:.2f})\n")

    return best_model


def main():
    print("Loading dataset and training ML model...")
    X, y = load_dataset("tictac_single.txt")
    model = train_model(X, y)
    game = Game(model)
    game.playGame()


if __name__ == "__main__":
    main()
