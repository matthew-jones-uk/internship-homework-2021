from pexhomework import __version__
from pexhomework import WordSearch


def test_version():
    assert __version__ == "0.0.1"


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
        assert ws.is_present(word)


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
        assert ws.is_present(word)
