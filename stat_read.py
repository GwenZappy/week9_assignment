import pandas as pd

# Load the game data from your log file (replace 'your_log_file.csv' with the actual file path)
log_file_path = '/Users/Administrator/Documents/01-GIX/TECHIN 509 Python/w9/logs/winners.csv'
df = pd.read_csv(log_file_path)

# Filter games by player type (HumanPlayer X, BotPlayer Y, HumanPlayer Y)
human_x_games = df[df['Player1_Type'] == 'human']
bot_y_games = df[df['Player1_Type'] == 'bot']
human_y_games = df[df['Player2_Type'] == 'human']

# Calculate statistics for each player type
def calculate_statistics(player_games):
    total_games = len(player_games)
    wins = len(player_games[player_games['Outcome'] == 'Player X wins!']) + len(player_games[player_games['Outcome'] == 'Player Y wins!'])
    draws = len(player_games[player_games['Outcome'] == "It's a tie!"])
    winning_percentage = (wins / total_games) * 100 if total_games > 0 else 0
    return total_games, wins, draws, winning_percentage

# Calculate statistics for each player type
human_x_stats = calculate_statistics(human_x_games)
bot_y_stats = calculate_statistics(bot_y_games)
human_y_stats = calculate_statistics(human_y_games)

# Create a DataFrame to display the statistics
statistics_df = pd.DataFrame({
    'Player Type': ['HumanPlayer X', 'BotPlayer Y', 'HumanPlayer Y'],
    'Total Games': [human_x_stats[0], bot_y_stats[0], human_y_stats[0]],
    'Wins': [human_x_stats[1], bot_y_stats[1], human_y_stats[1]],
    'Draws': [human_x_stats[2], bot_y_stats[2], human_y_stats[2]],
    'Winning Percentage': [human_x_stats[3], bot_y_stats[3], human_y_stats[3]]
})

# Sort the DataFrame by winning percentage to determine rankings
statistics_df = statistics_df.sort_values(by='Winning Percentage', ascending=False)

# Display the statistics table
print(statistics_df)

# Create plots to visualize the data (e.g., bar chart for wins, pie chart for draws)
# You can use Matplotlib or other plotting libraries for this part.
