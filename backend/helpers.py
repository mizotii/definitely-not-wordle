from collections import Counter
from typing import List

WORD_LENGTH = 5

def calc_char_freq_diff(guess, correct):
    return Counter(guess) - Counter(correct)

def guess_word(guess: str, answer: str) -> List[str]:
    res = ['none'] * WORD_LENGTH
    char_freq_count = Counter(answer)

    # first pass (green)
    for idx, (guess_c, cur_c)in enumerate(zip(guess, answer)):

        if guess_c == cur_c:
            res[idx] = 'green'
            char_freq_count[cur_c] -= 1

    # second pass (yellow)
    for idx, guess_c in enumerate(guess):
        if res[idx] == 'green':
            continue

        if char_freq_count[guess_c] > 0:
            res[idx] = 'yellow'
            char_freq_count[guess_c] -= 1

        else:
            res[idx] = 'gray'

    return res

def is_correct(result):
    return result == ['green'] * 5

def sanitize_guess(guess):
    if not (type(guess) == str and guess.isalpha() and len(guess) == WORD_LENGTH):
        return None
    
    return guess.upper().strip()