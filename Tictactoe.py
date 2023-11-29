from stats_manager import update_win_stats, save_stats_to_csv, read_stats_from_csv

class Board:
    def __init__(self):
        self.board = [" " for _ in range(9)]

    def print_board(self):
        for i in range(0, 9, 3):
            row = "|".join(str(j + 1) if self.board[j] == " " else self.board[j] for j in range(i, i + 3))
            print(row)
            if i < 6:
                print("-----")

    def is_valid_move(self, position):

        if 1 <= position <= 9:
            return self.board[position - 1] == " "
        return False

    def make_move(self, position, symbol):

        if self.is_valid_move(position):
            self.board[position - 1] = symbol
            return True
        return False

    def check_winner(self, symbol):

        # Check all winning conditions
        for i in range(3):
        # Check rows and columns
            if (
                self.board[i * 3]
                == self.board[i * 3 + 1]
                == self.board[i * 3 + 2]
                == symbol
            ) or (self.board[i] == self.board[i + 3] == self.board[i + 6] == symbol):
                return True
        # Check diagonals
        if (self.board[0] == self.board[4] == self.board[8] == symbol) or (
            self.board[2] == self.board[4] == self.board[6] == symbol
        ):
            return True
        return False

    def is_full(self):
        return all(cell != " " for cell in self.board)


class BasePlayer:
    def __init__(self, symbol, name):
        """Initializes the player with a symbol and name."""
        self.symbol = symbol
        self.name = name

    def make_move(self, board):
        pass

class HumanPlayer(BasePlayer):

    def make_move(self, board):

        try:
            position = int(input(f"Player {self.symbol}'s turn: "))
        except ValueError:
            return False
        return board.make_move(position, self.symbol)


class Game:

    def __init__(self, player1, player2):
        """Initializes the game with two players."""
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1

    def switch_player(self):
        """Switches the turn to the other player."""
        self.current_player = (
            self.player1 if self.current_player == self.player2 else self.player2
        )

    def play(self):
        while True:
            self.board.print_board()
            if not self.current_player.make_move(self.board):
                print("Invalid move, try again.")
                continue

            if self.board.check_winner(self.current_player.symbol):
                print(f"{self.current_player.name} wins!")
                update_win_stats(win_stats, self.current_player.name)
                break

            if self.board.is_full():
                self.board.print_board()
                print("It's a tie!")
                win_stats[self.player1.name]['ties'] += 1
                win_stats[self.player2.name]['ties'] += 1
                break

            self.switch_player()


if __name__ == "__main__":
    player1_name = input("Enter name for Player 1 (X): ")
    player2_name = input("Enter name for Player 2 (O): ")

    win_stats = read_stats_from_csv()  # Read existing stats or initialize if the file doesn't exist

    # Initialize stats for new players
    for player_name in [player1_name, player2_name]:
        if player_name not in win_stats:
            win_stats[player_name] = {'wins': 0, 'ties': 0, 'games_played': 0}

    player1 = HumanPlayer("X", player1_name)
    player2 = HumanPlayer("O", player2_name)

    game = Game(player1, player2)
    game.play()

    # Update games played count
    win_stats[player1_name]['games_played'] += 1
    win_stats[player2_name]['games_played'] += 1

    # Save updated statistics to CSV
    save_stats_to_csv(win_stats)

