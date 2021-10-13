class WordSearch:
    ROW_LENGTH: int = 8

    def __init__(self, grid: str) -> None:
        self.grid = grid

    def is_present(self, word: str) -> bool:
        for i in range(len(self.grid)):
            if self.grid[i] == word[0]:
                # we take the index after the index of the last letter of the word
                i_end_right = i + len(word)
                i_end_down = i + ((len(word) - 1) * self.ROW_LENGTH) + 1
                if (
                    self.grid[i:i_end_right] == word
                    and i // self.ROW_LENGTH == (i_end_right - 1) // self.ROW_LENGTH
                    and i_end_right - 1 < len(self.grid)
                ):
                    return True
                elif self.grid[
                    i : i_end_down : self.ROW_LENGTH
                ] == word and i_end_down - 1 < len(self.grid):
                    return True
        return False
