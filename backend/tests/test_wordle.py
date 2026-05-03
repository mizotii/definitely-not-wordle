import pytest
from unittest.mock import patch
from helpers import guess_word, is_correct, sanitize_guess, WORD_LENGTH
from wordle import WordList


@pytest.fixture
def words_file(tmp_path):
    f = tmp_path / "words.txt"
    f.write_text("CRANE\nSLATE\nADIEU\nSTORE\nBRASS\nCLASS\nNACRE\nCRARE\nSLATS\n")
    return f


@pytest.fixture
def word_list(words_file):
    with patch('wordle.WORD_LIST_FILEPATH', str(words_file)):
        wl = WordList()
    return wl


# --- word loading ---

def test_words_loaded_into_list_and_set(word_list):
    assert "CRANE" in word_list.words_list
    assert "CRANE" in word_list.words_set

def test_words_are_uppercased_on_load(word_list):
    assert all(w == w.upper() for w in word_list.words_list)


# --- WordList ---

def test_valid_word_is_accepted(word_list):
    assert word_list.is_valid_guess("CRANE") is True

def test_invalid_word_is_rejected(word_list):
    assert word_list.is_valid_guess("ZZZZZ") is False

def test_replace_current_answer_returns_word_from_list(word_list):
    answer = word_list.replace_current_answer()
    assert answer in word_list.words_set


# --- sanitize_guess ---

def test_sanitize_uppercases_guess():
    assert sanitize_guess("crane") == "CRANE"

def test_sanitize_rejects_non_alpha():
    assert sanitize_guess("CR4NE") is None

def test_sanitize_rejects_wrong_length():
    assert sanitize_guess("CAT") is None

def test_sanitize_rejects_non_string():
    assert sanitize_guess(12345) is None

def test_sanitize_rejects_spaces():
    assert sanitize_guess("CR AN") is None


# --- guess_word: green ---

def test_correct_guess_is_all_green():
    result = guess_word("CRANE", "CRANE")
    assert result == ['green'] * WORD_LENGTH

def test_correct_positions_are_green():
    result = guess_word("STORE", "STORE")
    assert result == ['green'] * WORD_LENGTH


# --- guess_word: yellow ---

def test_correct_letter_wrong_position_is_yellow():
    # Answer: CRANE, Guess: NACRE -> Y Y Y Y G
    result = guess_word("NACRE", "CRANE")
    assert result == ['yellow', 'yellow', 'yellow', 'yellow', 'green']


# --- guess_word: gray ---

def test_absent_letter_is_gray():
    result = guess_word("ZZZZZ", "CRANE")
    assert all(c == 'gray' for c in result)


# --- guess_word: duplicate letter handling ---

def test_extra_duplicate_gets_gray():
    # Answer: CRANE (one R). Guess: CRARE (two R's, first R is green at idx 1)
    result = guess_word("CRARE", "CRANE")
    assert result[1] == 'green'  # first R, correct position
    assert result[3] == 'gray'   # second R, no remaining count

def test_duplicate_in_answer_allows_yellow():
    # Answer: BRASS (two S's). Guess: SLATS
    result = guess_word("SLATS", "BRASS")
    assert result[0] == 'yellow'  # S present but wrong position
    assert result[4] == 'green'   # S at correct position


# --- is_correct ---

def test_is_correct_returns_true_for_all_green():
    assert is_correct(['green'] * 5) is True

def test_is_correct_returns_false_for_partial():
    assert is_correct(['green', 'yellow', 'green', 'green', 'green']) is False
