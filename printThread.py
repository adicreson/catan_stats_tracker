import threading
import time
from decimal import Decimal
import sys
from statusMessage import StatusMessage as Message
import datetime

def print_on_first_line(text):
    # Save the current cursor position
    sys.stdout.write('\033[s')

    # Move the cursor to the beginning of the line
    sys.stdout.write('\033[1;1H')

    # Clear the line
    sys.stdout.write('\033[2K')

    # Print the text on the first line
    sys.stdout.write(text)

    # Restore the cursor position
    sys.stdout.write('\033[u')

    sys.stdout.flush()

class PrintThread(threading.Thread):
    def __init__(self, fps, finished, num_players, messageQueue: list[Message], lock):
        threading.Thread.__init__(self)
        self.fps = fps
        self.finished = finished
        self.num_players = num_players
        self.messageQueue = messageQueue
        self.lock = lock

    def seconds_to_time_str(self, seconds): 
        return str(datetime.timedelta(seconds = seconds))

    def run(self):
        target_sleep_time = 1 / self.fps  # Assuming self.fps is a non-zero integer
        elapsed_time = 0
        start_time = time.time()
        cycles = 0
        throws = 0
        rounds = 0
        turn_time_stamp = 0
        round_time_stamp = 0
        
        while not self.finished:
            cycles += 1
            time.sleep(target_sleep_time * cycles  - elapsed_time)

            current_time = time.time()
            elapsed_time = current_time - start_time
            #print(elapsed_time)
            game_time = int(elapsed_time)
            turn_time = game_time - turn_time_stamp
            round_time = game_time - round_time_stamp

            if game_time % 1 == 0:
                print_on_first_line(f"Round: {rounds + 1}, Throws {throws}, Game Time: {self.seconds_to_time_str(game_time)}, Round Time: {self.seconds_to_time_str(round_time)}, Turn Time: {self.seconds_to_time_str(turn_time)}")

            
            if len(self.messageQueue) > 0:
                self.lock.acquire()
                message = self.messageQueue.pop(0)
                self.lock.release()
                if message.game_finished:
                    self.finished = True
                else:
                    throws = message.throws
                    rounds = int(throws / self.num_players)
                    if throws % self.num_players == 0:
                        round_time_stamp = game_time
                    turn_time_stamp = game_time