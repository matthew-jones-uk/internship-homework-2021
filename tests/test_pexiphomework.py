from string import ascii_lowercase
from random import choice, randint
from pexhomework import __version__
from pexhomework import WordSearch


def test_version():
    assert __version__ == "0.0.1"


def test_empty():
    ws = WordSearch("")
    assert not ws.is_present("")
    assert not ws.is_present("test")
    assert not ws.is_present("a")


def test_single_letter():
    ws = WordSearch("a")
    assert ws.is_present("a")
    assert not ws.is_present("b")


def test_search_4x4():
    grid = "test" "este" "eder" "nest"
    words_to_find = ["test", "teen", "nest"]
    ws = WordSearch(grid)
    print(ws._grid)
    ws.ROW_LENGTH = 4
    for word in words_to_find:
        answer = ws.is_present(word)
        assert answer
        assert isinstance(answer, bool)
    answer = ws.is_present("alphabet")
    assert not answer
    assert isinstance(answer, bool)
    answer = ws.is_present("dan")
    assert not answer
    assert isinstance(answer, bool)


def test_search_8x8():
    words_to_find = [
        "program",
        "map",
        "lead",
        "pleasure",
        "screen",
        "metal",
        "republic",
    ]
    grid = "xprogramblxjtpaaleadnfxpfaknfmpalscreenzpulkjteqmrqweatyrepublic"

    ws = WordSearch(grid)
    for word in words_to_find:
        answer = ws.is_present(word)
        assert answer
        assert isinstance(answer, bool)


def test_search_10x10():
    words_to_find = [
        "gang",
        "bangles",
        "satellite",
        "grip",
        "minimum",
        "guarantee",
        "bible",
        "tram",
    ]
    grid = "dkfbasdfghpgmajklhbpiutnghgripgangtherbosrplaotylbsatellitemvnsstyrrlkbtasdfjaoieeeminimumdeasdfjklh"

    ws = WordSearch(grid)
    ws.ROW_LENGTH = 10
    for word in words_to_find:
        answer = ws.is_present(word)
        assert answer
        assert isinstance(answer, bool)


def _generate_random_grid(row_length: int, ignore: list[str] = []) -> str:
    """Generate a random grid of letters"""
    accepted_letters = list()
    for letter in ascii_lowercase:
        if letter not in ignore:
            accepted_letters.append(letter)
    return "".join(choice(accepted_letters) for _ in range(row_length ** 2))


def _get_word_from_grid(grid: WordSearch, vertical=False) -> str:
    i = randint(0, grid.ROW_LENGTH - 2)
    if vertical:
        return grid._grid[randint(0, i) :: grid.ROW_LENGTH].decode("ascii")
    return grid._grid[i : (i // grid.ROW_LENGTH + 1) * grid.ROW_LENGTH].decode("ascii")


def _auto_test_grid(
    row_length: int,
    included_words: int,
    fake_words: int,
):
    """Automatically a grid of given size with a given number of words in the grid, and a
    given number of fake words that are definitely not in the grid.
    """
    # Don't have this letter in the grid so that we can be sure no word exists with it in it
    to_ignore = choice(ascii_lowercase)
    ws = WordSearch(_generate_random_grid(row_length, ignore=[to_ignore]))
    # Words that are definitely in grid
    for _ in range(included_words):
        word = _get_word_from_grid(ws)
        answer = ws.is_present(word)
        assert answer
        assert isinstance(answer, bool)
    # Words that are definitely not in grid
    for _ in range(fake_words):
        # Add the excluded letter to the word so that it will never match
        word = to_ignore + "".join(
            [choice(ascii_lowercase) for _ in range(randint(0, ws.ROW_LENGTH - 1))]
        )
        answer = ws.is_present(word)
        assert not answer
        assert isinstance(answer, bool)


def test_search_autogen_1Kx1K():
    """Test with 1000x1000 grid and 10k words - 5k in the grid, 5k not in the grid"""
    _auto_test_grid(1000, 5000, 5000)


def test_search_autogen_10Kx10K():
    """Test with 10000x10000 grid and a million words - 500k in the grid, 500k not in the grid"""
    _auto_test_grid(10000, 500000, 500000)
