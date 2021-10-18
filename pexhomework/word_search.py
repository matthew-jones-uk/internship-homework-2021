from typing import Optional


class WordSearch:
    ROW_LENGTH: int = 8
    _column_major_grid_row_length: Optional[int] = None
    _column_major_grid: bytearray = bytearray()  #
    _grid: bytearray = bytearray()  # grid always be redefined in __init__ anyway

    def __init__(self, grid: str) -> None:
        self._grid = self._grid_to_bytearray(
            grid.lower()
        )  # it should be all lowercase, but just in case

    def _grid_to_bytearray(self, grid: str) -> bytearray:
        # encode the grid into ascii for the bytearray to minimise memory usage
        return bytearray(grid.encode("ascii"))

    def _generate_column_major_grid(self) -> None:
        """Convert the _grid bytearray from row major order into column major order and store as a
        flattened 1D array in _column_major_grid. Also set the _column_major_grid_row_length to the
        row length.
        """
        self._column_major_grid_row_length = self.ROW_LENGTH
        self._column_major_grid = bytearray()
        for i in range(self.ROW_LENGTH):
            self._column_major_grid.extend(self._grid[i :: self.ROW_LENGTH])

    def is_present(self, word: str) -> bool:
        """Check if a word is present in the grid from left-to-right or top-to-bottom.

        Args:
            word (str): Word to search for.

        Returns:
            bool: If the word exists in grid.
        """
        if (
            len(self._column_major_grid)
            == 0  # check if the column major grid has been generated
            or self._column_major_grid_row_length
            != self.ROW_LENGTH  # check if row length has been changed
        ):
            self._generate_column_major_grid()  # generate the column major grid
        if len(word) > self.ROW_LENGTH:  # check if the word is too long
            return False
        # check if the word is present in both grid forms
        for current_grid in (self._grid, self._column_major_grid):
            current_index = 0  # where to start the search from
            # this condition is only needed if a potential word found by find() ends at the very end of the grid
            while current_index < len(current_grid):
                found_index = current_grid.find(word.encode("ascii"), current_index)
                if found_index == -1:  # no word is found in the grid
                    break
                # get the index of the last letter of the word
                end_index = found_index + len(word) - 1
                # check if the first letter is on the same row as the last letter
                if found_index // self.ROW_LENGTH == end_index // self.ROW_LENGTH:
                    return True
                current_index = found_index + 1  # start from after the failed word
        return False
