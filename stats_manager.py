import csv
import os

def update_win_stats(win_stats, winner_name):
    win_stats[winner_name]['wins'] += 1

def save_stats_to_csv(win_stats, filename='winnerstats.csv', directory='logs'):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Path to save the CSV file
    filepath = os.path.join(directory, filename)

    # Calculate win-to-game ratio
    for player, stats in win_stats.items():
        if stats['games_played'] > 0:
            stats['win_ratio'] = stats['wins'] / stats['games_played']
        else:
            stats['win_ratio'] = 0

    # Sort players by win ratio

    sorted_stats = sorted(win_stats.items(), key=lambda x: (x[1]['win_ratio'], x[1]['wins']), reverse=True)

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Rank', 'Player Name', 'Wins', 'Ties', 'Games Played', 'Win Ratio'])

        rank = 1
        last_ratio = -1  # Initialize with a value that will not match any player's ratio
        for player, stats in sorted_stats:
            current_ratio = stats['win_ratio']

            # Update rank only if current ratio is different from last ratio
            if current_ratio != last_ratio:
                last_ratio = current_ratio
                current_rank = rank

            writer.writerow([current_rank, player, stats['wins'], stats['ties'], stats['games_played'], round(stats['win_ratio'], 2)])
            
            rank += 1  # Increment rank for the next iteration
     
            # Increment rank for the next player if the ratio is different
            rank += 1 if current_ratio != last_ratio else 0


def read_stats_from_csv(filename='winnerstats.csv', directory='logs'):
    filepath = os.path.join(directory, filename)
    stats = {}
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                player_name = row['Player Name']
                wins = int(row['Wins'])
                games_played = int(row['Games Played'])
                # Handle 'Ties' field if it exists, else default to 0
                ties = int(row.get('Ties', 0))
                
                stats[player_name] = {
                    'wins': wins,
                    'ties': ties,
                    'games_played': games_played
                }
    return stats


