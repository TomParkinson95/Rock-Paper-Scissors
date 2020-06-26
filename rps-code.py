import random
import time
# Originally created by Tom Eric Parkinson, June 2020.
# Above I imported random and time for my improvements to the code.
# This program plays a game of Rock, Paper, Scissors between two Players,
# and reports both Player's scores each round.

moves = ['rock', 'paper', 'scissors']


# The Player class is the parent class for all of the Players in this game
class Player:
    def __init__(self):
        self.last_move_played = ""
        self.next_move = ""
        self.round_played = 0

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass


# Added the random player to the game successfully.
class RandomPlayer(Player):
    def move(self):
        return random.choice(moves)


# Added the human player class so humans can play.
class HumanPlayer(Player):
    def move(self):
        my_move = ""
        while my_move not in moves:
            my_move = input("Please enter your move:\n")
        return my_move


class ReflectPlayer(Player):
    # The sets of if/else statements make the learn function for the
    # ReflectPlayer work differently. Comment them out and try them both!
    def learn(self, my_move, their_move):
        if beats(their_move, my_move) is True:
            self.next_move = their_move
        else:
            self.next_move = my_move
        # if my_move != their_move:
        #     self.next_move = their_move
        # else:
        #     self.next_move = random.choice(moves)

    def move(self):
        if self.next_move == "":
            return random.choice(moves)
        else:
            return self.next_move


class CyclePlayer(Player):
    def learn(self, my_move, their_move):
        self.round_played += 1
        if self.round_played > 2:
            self.round_played = 0

    def move(self):
        return moves[self.round_played]


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        # Added scores and number of rounds to the game.
        self.p1.score = 0
        self.p2.score = 0
        while True:
            try:
                self.rounds = int(input("How many rounds do "
                                        "you want to play?\n"))
                break
            except ValueError:
                print_pause("Not a valid number. Please try again.")

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print_pause(f"Player 1: {move1}  Player 2: {move2}")
        if beats(move1, move2) is True:
            self.p1.score += 1
            print_pause("Player 1 wins the round!")
        elif move1 == move2:
            print_pause("Tie round! No points awarded!")
        else:
            self.p2.score += 1
            print_pause("Player 2 wins the round!")
        print("Player 1 score: " + str(self.p1.score),
              "Player 2 score: " + str(self.p2.score))
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def play_game(self):
        print_pause("Game start!")
        # Improved the rounds with a while loop.
        round_count = 0
        while round_count < self.rounds:
            round_count += 1
            print_pause(f"Round {round_count}:")
            self.play_round()
        if self.p1.score > self.p2.score:
            print_pause("Player 1 wins the game!")
        elif self.p1.score == self.p2.score:
            print_pause("Tie game! Well done both of you!")
        else:
            print_pause("Player 2 wins the game!")
        print_pause(f"Final score - Player 1: {self.p1.score}"
                    f" Player 2: {self.p2.score}")
        print_pause("Player 1 K/D: "
                    f"{round(kd(self.p1.score, self.p2.score), 4)}"
                    " Player 2 K/D: "
                    f"{round(kd(self.p2.score, self.p1.score), 4)}")
        print_pause("Game over!")


# Checks which player won the game.
def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


# Added this for a nice delay in messages to make the game more readable.
def print_pause(msg):
    time.sleep(1)
    print(msg)


# Outputs the K/D ratio at the end of a game.
def kd(p1_wins, p2_wins):
    try:
        return p1_wins / p2_wins
    except ZeroDivisionError:
        if p1_wins <= 0:
            return ((p1_wins + 0.01) * 100) / p2_wins
        elif p2_wins <= 0:
            return p1_wins / ((p2_wins + 0.01) * 100)


if __name__ == '__main__':
    # Add different pairs of players here to test the game.
    game = Game(HumanPlayer(), ReflectPlayer())
    game.play_game()
