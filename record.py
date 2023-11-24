import csv
import os
from Tictactoe import BotPlayer, HumanPlayer, Board, Game

class WinnersDatabase:
    def __init__(self, filename="logs/winners.csv"):
        self.filename = filename
        self.fieldnames = ["Player", "Symbol", "Player_Type"]

        # Create the logs directory if it doesn't exist
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        # Create the CSV file if it doesn't exist
        if not os.path.isfile(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

    def add_winner(self, player):
        player_type = "human" if isinstance(player, HumanPlayer) else "bot"
        with open(self.filename, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow({"Player": player.symbol, "Symbol": player.symbol, "Player_Type": player_type})

    def add_tie(self):
        with open(self.filename, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow({"Player": "Tie", "Symbol": "Tie", "Player_Type": "Tie"})


class Game:
    def __init__(self, player1, player2, winners_database):
        """Initializes the game with two players."""
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.winners_database = winners_database

    def switch_player(self):
        """Switches the turn to the other player."""
        self.current_player = (
            self.player1 if self.current_player == self.player2 else self.player2
        )

    def play(self):
        # Run the game loop
        while True:
            self.board.print_board()
            if not self.current_player.make_move(self.board):
                print("Invalid move, try again.")
                continue

            if self.board.check_winner(self.current_player.symbol):
                self.board.print_board()
                print(f"Player {self.current_player.symbol} wins!")
                self.winners_database.add_winner(self.current_player)
                break

            if self.board.is_full():
                self.board.print_board()
                print("It's a tie!")
                self.winners_database.add_tie()
                break

            self.switch_player()

if __name__ == "__main__":
    # To play the game
    while True:
        num_human_players = input("How many human players? (1/2): ")
        if num_human_players in ["1", "2"]:
            break
        else:
            print("Please only enter 1 or 2.")

    player1 = HumanPlayer("X")
    player2 = BotPlayer("O")

    if num_human_players == "1":
        player2 = BotPlayer("O")
    elif num_human_players == "2":
        player2 = HumanPlayer("O")

    winners_database = WinnersDatabase()

    game = Game(player1, player2, winners_database)
    game.play()