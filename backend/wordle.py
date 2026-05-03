import os
import random
from typing import List, Set

WORD_LENGTH = 5
WORD_LIST_FILEPATH = os.environ.get('WORD_LIST_FILEPATH', './words.txt')

class WordList:
    def __init__(self):
        self.words_list: List[str] = []
        self.words_set: Set[str] = set()

        self._load_words()
        
    def is_valid_guess(self, guess: str):
        return guess in self.words_set

    def replace_current_answer(self):
        return random.choice(self.words_list)

    def _load_words(self):
        with open(WORD_LIST_FILEPATH, 'r') as f:
            lines = f.readlines()
            for line in lines:
                word = line.strip().upper()
                self.words_list.append(word)
                self.words_set.add(word)