import datetime
from catanStatsPlotter import CatanStatsPlotter
from statusMessage import StatusMessage as Message
from printThread import PrintThread
from player import Player
import time
import os
import threading

def clear_terminal():
    # Clear terminal screen for different operating systems
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and Mac
        os.system('clear')


def clear_terminal_except_first_line():
    # Clear the terminal screen
    os.system('clear')  # For Linux/macOS
    # os.system('cls')  # For Windows

    # Move the cursor to the first line
    print('\033[1;1H', end='')

    # Print empty lines to push previous content out of view
    terminal_height = os.get_terminal_size().lines
    for _ in range(terminal_height - 1):
        print()
    
    #Move cursor to beginning of second line
    print('\033[2;1H', end='')

class Game:
    def __init__(self):
        self.players = []
        self.finished = False
        self.winner = None
        self.rounds = 0
        self.throws = []
        self.total_time = 0
        self.catanStatsPlotter = CatanStatsPlotter()
        self.message_queue: list[Message] = []
        self.lock = threading.Lock()
    
    def add_player(self, name, isFirst=False):
            player = Player(name, isFirst, self.message_queue, self.lock)
            self.players.append(player)

    def add_players(self):
        while True:
            num_players_input = input("Enter the number of players in playing order (minimum 2, maximum 4): ")
            try:
                num_players = int(num_players_input)
                if 2 <= num_players <= 4:
                    break  # Exit the loop if a valid number of players is provided
                else:
                    print("Invalid number of players. Maximum allowed is 4. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        print(f"Number of players: {num_players}")
        for i in range(num_players):
            player_name = input(f"Enter the name of Player {i+1}: ")
            if i == 0:
                self.add_player(player_name, isFirst=True)  # Set isFirst=True for the first player
            else:
                self.add_player(player_name)

    def get_throw_count(self):
        return len(self.throws)
    
    def seconds_to_time_str(self, seconds):
        seconds = round(seconds)
        return str(datetime.timedelta(seconds = seconds))

    def play_round(self):
        for player in self.players:
            start = time.time()
            throw = player.record_turn()
            if throw == -1:
                self.finished = True
                break
            self.throws.append(throw)
            num_throws = self.get_throw_count()
            message = Message(False, num_throws)
            self.lock.acquire()
            self.message_queue.append(message)
            self.lock.release()
            round_time = time.time() - start
            player.add_time(round_time)
            self.total_time += round_time
        clear_terminal_except_first_line()


    def print_results(self):
        clear_terminal()

        print("Game finished!")
        print("Below are the statistics for the game:")
        print(f"Total rounds: {self.rounds}")
        print(f"Total throws: {self.get_throw_count()}")
        total_time = self.seconds_to_time_str(self.total_time)
        print(f"Total time: {total_time}")

        for player in self.players:
            print("\nPlayer:", player.name)
            print("Throws:", player.get_throw_count())
            total_time = self.seconds_to_time_str(player.total_time)
            print("Total time:", total_time)
            average_time = self.seconds_to_time_str(player.get_average_time_per_throw())
            print("Average time per throw:", average_time)


    
    def start(self):
        clear_terminal()
        print("Game started!")
        #Gameloop
        self.add_players()
        clear_terminal()
        printThread = PrintThread(20, False, len(self.players), self.message_queue, self.lock)
        printThread.start()

        while not self.finished:
            self.rounds += 1
            self.play_round()

            if(self.finished):
                printThread.join()
                self.print_results()
                self.catanStatsPlotter.plot_stats(self)
                break

            
def main():
        game = Game()
        game.start()


if __name__ == "__main__":
    main()