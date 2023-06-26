# Catan Statistics Tracker
Where you lucky or not? Use the following program to track a couple of metrics while playing a game, such as throws and time per round. Primarily used to track the outcome of the throws and then compare it to their theoretical values.

## Game
Represents a game of Catan. Manages players, records throws, calculates statistics, and displays results.

## CatanStatsPlotter
Responsible for plotting the statistics of throw values in a game of Catan, comparing it to the theoretical values.

## Player
Represents a player in the game of Catan.

## PrintThread
Displays real-time game information in the terminal using a separate thread.

## StatusMessage
A class used as a type for communicating game status between threads.

## How to Start the Game
To start the game, follow these steps:

Install python and the necessary dependencies. Open a terminal and write "python3 game.py".

The game will prompt you to enter the number of players and their names. After that, the game will proceed with each player taking turns recording their throws. To quit the game, enter 'q' when prompted for a throw value.

Once the game is finished, it will display the game statistics, including the total rounds, total throws, and total time. It will also plot the statistics of throw values using the CatanStatsPlotter class.

Ensure that you have a compatible Python environment set up and all the required files are in the same directory before starting the game.