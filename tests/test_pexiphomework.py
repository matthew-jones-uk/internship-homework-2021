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
