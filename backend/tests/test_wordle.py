import pytest
from unittest.mock import patch
from wordle import WordlePlayer, Color, MAX_TURNS, WORD_LENGTH


@pytest.fixture
def player(tmp_path):
    words_file = tmp_path / "words.txt"
    words_file.write_text("CRANE\nSLATE\nADIEU\nSTORE\nBRASS\nCLASS\nNACRE\nCRARE\nSLATS\n")
    with patch("random.choice", return_value="CRANE"):
        p = WordlePlayer(str(words_file))
    return p


# --- word loading ---

def test_words_loaded_into_list_and_set(player):
    assert "CRANE" in player.words_list
    assert "CRANE" in player.words_set

def test_words_are_uppercased_on_load(player):
    assert all(w == w.upper() for w in player.words_list)


# --- validation ---

def test_valid_word_is_accepted(player):
    result = player.guess_word("CRANE")
    assert result != [Color.NONE] * WORD_LENGTH

def test_invalid_word_returns_all_none(player):
    result = player.guess_word("ZZZZZ")
    assert result == [Color.NONE] * WORD_LENGTH

def test_guess_is_case_insensitive(player):
    lower = player.guess_word("crane")
    upper = player.guess_word("CRANE")
    assert lower == upper

def test_guess_is_stripped(player):
    result = player.guess_word("  CRANE  ")
    assert result != [Color.NONE] * WORD_LENGTH


# --- scoring: green ---

def test_correct_guess_is_all_green(player):
    result = player.guess_word("CRANE")
    assert result == [Color.GREEN] * WORD_LENGTH

def test_correct_positions_are_green(player):
    # CRANE vs STORE: R is at index 1 in CRANE, index 2 in STORE -- no greens expected
    with patch.object(player, "current_word", "STORE"):
        result = player.guess_word("STORE")
    assert result == [Color.GREEN] * WORD_LENGTH


# --- scoring: yellow ---

def test_correct_letter_wrong_position_is_yellow(player):
    # Answer: CRANE, Guess: NACRE -> Y Y Y Y G
    # E at idx 4 matches -> green; N,A,C,R all present but wrong position -> yellow
    with patch.object(player, "current_word", "CRANE"):
        result = player.guess_word("NACRE")
    assert result == [Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.GREEN]


# --- scoring: duplicate letter handling ---

def test_extra_duplicate_gets_gray(player):
    # Answer: CRANE (one R). Guess: CRARE (two R's, first R is green at idx 1)
    # Second R at idx 3 should be gray since answer has no remaining R
    with patch.object(player, "current_word", "CRANE"):
        result = player.guess_word("CRARE")
    assert result[1] == Color.GREEN   # first R, correct position
    assert result[3] == Color.GRAY    # second R, no remaining count

def test_duplicate_in_answer_allows_yellow(player):
    # Answer: BRASS (two S's). Guess: SLATS (one S at idx 0, one S at idx 4)
    with patch.object(player, "current_word", "BRASS"):
        result = player.guess_word("SLATS")
    # S at idx 0: not green (answer[0]=B), but answer has S's remaining -> yellow
    assert result[0] == Color.YELLOW
    # S at idx 4: answer[4]=S -> green
    assert result[4] == Color.GREEN


# --- reset ---

def test_reset_sets_turn_to_zero(player):
    player.current_turn = 3
    player._reset_game()
    assert player.current_turn == 0

def test_reset_replaces_current_word(player):
    old_word = player.current_word
    with patch("random.choice", return_value="SLATE"):
        player._reset_game()
    assert player.current_word == "SLATE"
