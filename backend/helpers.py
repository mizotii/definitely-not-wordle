from collections import Counter

def calc_char_freq_diff(guess, correct):
    return Counter(guess) - Counter(correct)
