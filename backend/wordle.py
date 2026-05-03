import random
from collections import Counter
from enum import Enum
from helpers import calc_char_freq_diff
from typing import List, Set

MAX_TURNS = 6
WORD_LENGTH = 5

class Color(Enum):
    NONE = 0
    GRAY = 1
    YELLOW = 2
    GREEN = 3

class WordlePlayer:
    def __init__(self, words_filepath):
        # data
        self.words_filepath: str = words_filepath
        self.words_list: List[str] = []
        self.words_set: Set[str] = set()

        # game state
        self.current_word: str = ''
        self.current_turn: int = 0
        self.max_turns: int = MAX_TURNS

        self._load_words()
        self._reset_game()

    def guess_word(self, guess: str) -> List[Color]:
        guess = guess.upper().strip()

        res = [Color.NONE] * WORD_LENGTH
        char_freq_count = Counter(self.current_word)

        if self._is_valid_guess(guess):
            # first pass (green)
            for idx, (guess_c, cur_c)in enumerate(zip(guess, self.current_word)):

                if guess_c == cur_c:
                    res[idx] = Color.GREEN
                    char_freq_count[cur_c] -= 1

            print(char_freq_count)

            # second pass (yellow)
            for idx, guess_c in enumerate(guess):
                if res[idx] == Color.GREEN:
                    continue

                if char_freq_count[guess_c] > 0:
                    res[idx] = Color.YELLOW
                    char_freq_count[cur_c] -= 1

                else:
                    res[idx] = Color.GRAY

        return res
        
    def _is_valid_guess(self, guess: str):
        return guess in self.words_set

    def _reset_game(self):
        self.current_turn = 0
        self._replace_current_word()

    def _replace_current_word(self):
        self.current_word = random.choice(self.words_list)

    def _load_words(self):
        with open(self.words_filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                word = line.strip().upper()
                self.words_list.append(word)
                self.words_set.add(word)