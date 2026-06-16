from english_words import get_english_words_set


import random


#import re


def input_loop():
    """Input loop for accepted letters. Returns a list that is either empty or contains one lowercase letter."""
    loop_valid_character_finder = None
    loop_letter = input("Enter a letter:").lower().strip()
    # loop_valid_character_finder = re.findall("^[A-z]$", loop_letter)
    valid_letters = list("abcdefghijklmnopqrstuvwxyz")
    if len(loop_letter) == 1 and loop_letter in valid_letters:
        loop_valid_character_finder = loop_letter
    return loop_valid_character_finder

def main_game_loop(current_word, trial_attempts, joined_display):
    while len(current_word) < 5:
        if trial_attempts >= 3:
            print("Maximum allowed attempts for one letter input exceeded.")
            exit(0)

        current_letter = input_loop()

        if current_letter is not None: #if the list of current letter isn't empty)
            current_word += current_letter
            trial_attempts = 0
            for i, letter in enumerate(letter_display): #enumerate gets index and value together
                if letter == "_":
                    letter_display[i] = current_letter
                    joined_display = " ".join(letter_display)
                    break

            print(f"Current entry: {joined_display}")
            # print(f"{current_letter} is the current letter")
              # test code
            # print(f"length current word: {len(current_word)}")

        else:
            print("Input is not a valid uppercase or lowercase letter")
            trial_attempts = trial_attempts + 1
            print(f"Attempts currently made for a letter: {trial_attempts}")
            print(f"{joined_display} is the current word")

    print("Maximum allowed letters reached. Checking your answer now:")
    return(current_word)


def solution_match_checker(user_word, random_solution, previous_attempts, correct_display):
    """Checks if the user input word matches the solution."""

    # print(f"random word: {random_solution}")

    user_letters = list(user_word)
    solution_letters = list(random_solution)

    if user_word == random_solution:
        print(f"Correct! The answer is {random_solution}.")
        exit(0)
    else:
        print(f"Your answer of {user_word} is incorrect.")
        contains_display = []
        if correct_display == []:
            for i, letter in enumerate(solution_letters):
                if user_letters[i] == letter:
                    correct_display.append(letter)
                else:
                    correct_display.append("_")
        else:
            for i, letter in enumerate(solution_letters):
                if correct_display[i] == "_":
                    if user_letters[i] == letter:
                        correct_display[i] = letter

        previous_attempts.append(current_word)
        print(f"Your past attempts were: {previous_attempts}")

        previous_copy = previous_attempts[:]
        for letter in solution_letters:
            for i, attempts in enumerate(previous_attempts):
                if letter in attempts:
                    contains_display.append(letter)
                    previous_copy[i] = previous_copy[i].replace(letter, "")

        incorrect_letters = []
        for attempt in previous_copy:
            for letters in attempt:
                incorrect_letters.append(letters)
        print(f"Your current correct letters: {list(correct_display)}")
        contains_display = list(set(contains_display))
        print(f"The answer contains: {contains_display}")
        incorrect_letters = list(set(incorrect_letters))
        print(f"The answer does not contain: {incorrect_letters}")



if __name__ == '__main__':
    user_reached_solution = False
    attempts = 0
    all_words = get_english_words_set(['web2'], lower=True)
    five_letter_words = [word for word in all_words if len(word) == 5 and word.isalpha()]
    # random_solution = five_letter_words[random.randint(0, len(five_letter_words) - 1)]
    random_solution = "apple"
    previous_attempts = []

    while not user_reached_solution and attempts < 6:
        current_word = ""
        trial_attempts = 0
        letter_display = ["_", "_", "_", "_","_"]
        joined_display = " ".join(letter_display)
        if attempts == 0:
            correct_display = []
        current_word = main_game_loop(current_word, trial_attempts, joined_display)

        if current_word in five_letter_words:
            solution_match_checker(current_word, random_solution, previous_attempts, correct_display)
            attempts += 1
            print(f"Current attempts: {attempts}")
        else:
            print("Please enter a valid english word.")

    print("Maximum allowed attempts exceeded.")
    print(f"The correct word was {random_solution}.")
    exit(0)





