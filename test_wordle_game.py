import pytest



from unittest.mock import patch



from wordle_game import Wordle

class TestWordle:
    def test_initialization(self):
        game = Wordle(pool_size=100, word_length=5)

        #assert: does nothing if true. raises AssertionError if false
        assert game.word_length == 5
        assert len(game.solution_pool) == 100
        assert game.random_solution in game.solution_pool

    #test valid input
    @patch('builtins.input', return_value="apple")
    def test_input_loop_valid(self, _mock_input):
        game = Wordle()
        game.input_loop() #normally where program is paused, and user input is entered, @patch returns string "apple"
        #instead. it "pretends" like the user just typed apple

        assert game.current_word == "apple" #checks to see if the user typed apple, current_word is set to apple

    @patch('builtins.input', return_value="APPLE")
    def test_input_loop_uppercase(self, _mock_input):
        game = Wordle()
        game.input_loop()

        assert game.current_word == "apple"

    #test invalid input
    @patch('builtins.input', return_value="cat")
    def test_input_loop_invalid(self, _mock_input):
        game = Wordle()
        game.input_loop()

        assert game.current_word is None


    @patch('builtins.input', return_value="a@ple")
    def test_input_loop_special_characters(self, _mock_input):
        game = Wordle()
        game.input_loop()

        assert game.current_word is None

    def test_solution_match_checker_duplicate_letters(self):
        game = Wordle()
        game.random_solution = "apple"
        game.current_word = "paper"

        game.solution_match_checker()

        assert game.correct_display == ["_", "_", "p", "_", "_"]

        assert "p" in game.contains_display
        assert "a" in game.contains_display
        assert "e" in game.contains_display

        assert "r" in game.incorrect_display

    #test repeated invalid inputs
    @patch('builtins.input', side_effect=["cat", "dog", "rat"])
    #side_effect - feature that changes behavior of mock object each time it is called
    #main_game_loop has a while loop that repeatedly calls input. side_effect passes cat, dog, rat into it each time
    #side_effect can also be used to crash a mocked function, trigger a custom function
    def test_main_game_loop_max_trials_exceeded(self, _mock_input):
        game = Wordle()
        with pytest.raises(SystemExit) as exit_state:
            game.main_game_loop()
        assert exit_state.value.code == 0
        assert game.trial_attempts == 3

    #test repeated wrong guesses
    @patch('builtins.input', side_effect=["bacon", "bacon", "bacon", "bacon", "bacon", "bacon"])
    def test_play_game_loss_condition(self, _mock_input):
        game = Wordle()
        game.random_solution = "apple"

        #is it in top 2000 of frequent words?
        game.all_words.append("bacon")

        with pytest.raises(SystemExit) as exit_state:
            game.play_game(
            )

        assert exit_state.value.code == 0
        assert game.solution_attempts == 6

    #test non-word entry
    @patch('builtins.input', side_effect=["qxzjq"])
    def test_play_game_invalid_english_word(self, _mock_input):
        game = Wordle()
        game.random_solution = "apple"

        #StopIteration: pytest.raises parameter that stops as soon as side_effect runs out of items in the list
        #to prevent infinite looping
        with pytest.raises(StopIteration):
            game.play_game()

        assert game.solution_attempts == 0
    #test incorrect guess
    def test_solution_match_checker_incorrect(self):
        game = Wordle()

        #fake input and solution
        game.random_solution = "apple"
        game.current_word = "alert"

        game.solution_match_checker()

        assert game.correct_display == ["a", "_", "_", "_","_"]
        assert "l" in game.contains_display
        assert "e" in game.contains_display
        assert "r" in game.incorrect_display
        assert "t" in game.incorrect_display
        assert "alert" in game.previous_attempts

    #test correct guess
    def test_solution_match_checker_correct(self):
        game = Wordle()
        game.random_solution = "apple"
        game.current_word = "apple"

        with pytest.raises(SystemExit) as exit_state:
            #pytest.raises: pytest tool to "catch" an exception instead of the exception actually stopping the program
            #exit() raises SystemExit exception. with statement saves data of SystemExit in exit_state variable
            game.solution_match_checker()

        assert exit_state.value.code == 0 #this checks that the value of exit() was 0, which it should be