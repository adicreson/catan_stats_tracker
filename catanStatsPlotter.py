import pandas as pd
import matplotlib.pyplot as plt

class CatanStatsPlotter:
    def __init__(self):
        self.theoretical_probabilities = {
            2: 1 / 36,
            3: 2 / 36,
            4: 3 / 36,
            5: 4 / 36,
            6: 5 / 36,
            7: 6 / 36,
            8: 5 / 36,
            9: 4 / 36,
            10: 3 / 36,
            11: 2 / 36,
            12: 1 / 36
        }

    def plot_stats(self, game):
        # Create a dataframe with the throws for each player
        df = pd.DataFrame()

        throw_count = {player.name: player.get_throw_count() for player in game.players} 
        throw_count["Game"] = game.get_throw_count()

        # Create a column for each player name
        for player in game.players:
            # Get the throws for the current player
            throws = player.get_throws()

            # Count the number of occurrences of each throw value
            throws_counts = {throw: throws.count(throw) for throw in range(2, 13)}

            # Add the player's throws counts to the dataframe
            df[player.name] = pd.Series(throws_counts)

        # Calculate the total occurrences for each throw value
        total_occurrences = df.sum(axis=1)

        # Add the 'Game' column representing total occurrences
        df['Game'] = total_occurrences

        # Determine the number of subplots based on the number of columns
        num_subplots = len(df.columns)

        # Calculate the number of rows and columns for the grid layout
        num_rows = int(num_subplots / 2) + (num_subplots % 2)
        num_cols = 2

        # Create a figure and subplots for the grid layout
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
        fig.suptitle('Occurrences of Throw Values', fontsize=16)

        # Flatten the axes array if it's a single row or column
        axes = axes.flatten() if num_subplots > 1 else [axes]

        # Plot each column in a separate subplot
        for i, column in enumerate(df):
            ax = axes[i]
            df[column].plot(kind='bar', ax=ax)
            ax.set_xlabel('Throw Value')
            ax.set_ylabel('Occurrences')
            ax.set_title(column)

            # Add theoretical distribution to the plot
            theoretical_probabilities = self.theoretical_probabilities
            dim = len(theoretical_probabilities)
            #ax.plot(theoretical_probabilities.keys(), theoretical_probabilities.values(), 'r', label='Theoretical')
            ax.plot(list(range(0,dim)), [prob * throw_count[column] for prob in theoretical_probabilities.values()], 'r', label='Theoretical')

            ax.legend()

        # Adjust the layout and display the plot
        plt.tight_layout()
        plt.show()
