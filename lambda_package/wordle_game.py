import random
from typing import List

from wordfreq import iter_wordlist #iter_wordlist function iterates through all english words in order of frequency
#wordfreq library provides pre-compiled word frequency data
#data science side project ?


class Wordle:

    def __init__(self, pool_size=2000, word_length=5, max_solution_attempts=6, max_trial_attempts=3):
        self.all_words = [word for word in iter_wordlist('en') if len(word) == word_length and word.isalpha()] #this is called list comprehension, also works for tuples, dictionary
        self.word_length = word_length
        self.solution_pool = self.get_solution_pool(pool_size)
        self.current_word = None
        self.random_solution = random.choice(self.solution_pool)
        self.max_solution_attempts = max_solution_attempts
        self.max_trial_attempts = max_trial_attempts

        self.trial_attempts = 0
        self.solution_attempts = 0

        self.previous_attempts = []
        self.correct_display = ["_"] * word_length
        self.contains_display = []
        self.incorrect_display = []
        self.user_reached_solution = False


    def get_solution_pool(self, pool_size=2000):
        """Get most common {word_length}-letter words to use as answer key."""
        pool = []
        for word in iter_wordlist('en'):
            if len(word) == self.word_length and word.isalpha():
                pool.append(word)
            if len(pool) == pool_size:
                break
        return pool


    def input_loop(self):
        """Input loop for accepted letters. Returns a list that is either empty or contains one lowercase string."""
        self.current_word = input(f"Enter a {self.word_length}-letter word:").lower().strip()
        self.current_word = self.current_word if len(self.current_word) == self.word_length and set(self.current_word).issubset(set("abcdefghijklmnopqrstuvwxyz")) else None  #walrus sign can make this one line

    @staticmethod
    def check_input(user_input: str, daily_solution: str) -> Lgaist[int]:
        """Checks a user input and returns a list of integers based on correct/incorrect letters and position."""
        letter_colors = [0] * 5
 #apple
        for i, letter in enumerate(user_input): #apple
            if letter in daily_solution: #alert 2 1 1 0 0
                if user_input[i] == daily_solution[i]:
                    letter_colors[i] = 2 #green
                else :
                    letter_colors[i] = 1 #yellow
        return letter_colors


    def main_game_loop(self):
        self.trial_attempts = 0

        while self.trial_attempts < self.max_trial_attempts:
            self.input_loop()
            if self.current_word is None:  # if the list of current letter isn't empty)
                print("Input is not exactly 5 letters.")
                self.trial_attempts = self.trial_attempts + 1
                print(f"Attempts currently made for an entry: {self.trial_attempts}")

            else:
                print(f"Current entry: {self.current_word}")
                return
        print("Maximum allowed attempts for one input exceeded.")
        exit(0)

    def solution_match_checker(self) -> None:
        """Checks if the user input word matches the solution."""

        if self.current_word == self.random_solution:
            print(f"Correct! The answer is {self.random_solution}.")
            exit(0)
        else:
            print(f"Your answer of {self.current_word} is incorrect.")

            for i,(solution_letter, input_letter) in enumerate(zip(self.random_solution, self.current_word)):
                if solution_letter == input_letter:
                    self.correct_display[i] = solution_letter
                else:
                    self.correct_display[i] = "_"

            self.previous_attempts.append(self.current_word) #apple
            print(f"Your past attempts were: {self.previous_attempts}")

            for letter in self.current_word:
                if letter in self.random_solution:
                    self.contains_display.append(letter)
                else:
                    self.incorrect_display.append(letter)


            print(f"Your current correct letters: {list(self.correct_display)}")
            print(f"The answer contains: {list(set(self.contains_display))}")
            print(f"The answer does not contain: {list(set(self.incorrect_display))}")

    def play_game(self):
        while not self.user_reached_solution and self.solution_attempts < self.max_solution_attempts:
            self.main_game_loop()
            if self.current_word in self.all_words:
                self.solution_match_checker()
                self.solution_attempts += 1
                print(f"Current attempts: {self.solution_attempts}")
            else:
                print("Please enter a valid english word.")

        print("Maximum allowed attempts exceeded.")
        print(f"The correct word was {self.random_solution}.")
        exit(0)


if __name__ == '__main__':
    game_settings = {"pool_size": 2000, "word_length": 5, "max_solution_attempts": 6, "max_trial_attempts": 3}
    game1 = Wordle(**game_settings) #**this unpacks game_settings the dictionary to keyword arguments. single star (*) unpacks tuples
    game1.play_game()






