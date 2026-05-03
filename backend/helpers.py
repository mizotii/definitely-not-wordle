from collections import Counter
from enum import Enum
from typing import List

WORD_LENGTH = 5

class Color(Enum):
    NONE = 0
    GRAY = 1
    YELLOW = 2
    GREEN = 3

def calc_char_freq_diff(guess, correct):
    return Counter(guess) - Counter(correct)

def guess_word(guess: str, answer: str) -> List[Color]:
    res = [Color.NONE] * WORD_LENGTH
    char_freq_count = Counter(answer)

    # first pass (green)
    for idx, (guess_c, cur_c)in enumerate(zip(guess, answer)):

        if guess_c == cur_c:
            res[idx] = Color.GREEN
            char_freq_count[cur_c] -= 1

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

def is_correct(result):
    return result == [Color.GREEN] * 5