from statusMessage import StatusMessage as Message


def print_on_pos(content, row, col):
    # Move the cursor to the second line using ANSI escape sequence
    print(f"\033[{row};{col}H", end="")
    # Print the input prompt
    inp = input(content)
    return inp


class Player:
    def __init__(self, name, isFirst, messageQueue: list[Message], lock):
        self.name = name
        self.points = 0
        self.hasWon = False
        self.throws = []
        self.times  = []
        self.total_time = 0
        self.messageQueue = messageQueue
        self.isFirst = isFirst
        self.lock = lock
        self.game_finished = False

    def record_throw(self):
        print_on_first_row = True
        throw = None
        while throw is None:
            if self.isFirst and print_on_first_row:
                inp = print_on_pos(f"Enter the throw for {self.name}: ", 2, 1)
            else:
                inp = input(f"Enter the throw for {self.name}: ")
    
            if inp == "q":
                message = Message(True, 0)
                self.lock.acquire()
                self.messageQueue.append(message)
                self.lock.release()
                self.game_finished = True
                return -1
    
            if inp.isdigit():
                throw = int(inp)
                if 2 <= throw <= 12:
                    self.throws.append(throw)
                    return throw
    
            print("Invalid throw. Please enter a value between 2 and 12.")
            print_on_first_row = False
            throw = None  # Set throw to None to continue the loop



    def record_points(self):
        while True:
            try:
                points = int(input(f"Enter the points for {self.name}: "))
                if points >= 0:
                    self.points = points
                    if points >= 10:
                        self.hasWon = True
                    break  # Exit the loop if a valid number is entered
                else:
                    print("Invalid input. Please enter a non-negative number.")
            except ValueError:
                print("Invalid input. Please enter a number.")


    def record_turn(self):
        throw = self.record_throw()
        #self.record_points()

        return throw

    def add_time(self, time):
        self.times.append(time)
        self.total_time += time
        
    def get_points(self):
        return self.points

    def get_throw_count(self):
        return len(self.throws)

    def get_throws(self):
        return self.throws
    
    def get_average_time_per_throw(self):
        return self.total_time / len(self.throws)