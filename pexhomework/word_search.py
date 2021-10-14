from typing import Optional


class WordSearch:
    ROW_LENGTH: int = 8
    _column_major_grid_row_length: Optional[int] = None
    _column_major_grid: bytearray = bytearray()
    _grid: bytearray = bytearray()

    def __init__(self, grid: str) -> None:
        self._grid = self._grid_to_bytearray(
            grid.lower()
        )  # it should be all lowercase, but just in case

    def _grid_to_bytearray(self, grid: str) -> bytearray:
        return bytearray(grid.encode("ascii"))

    def _generate_column_major_grid(self) -> None:
        self._column_major_grid_row_length = self.ROW_LENGTH
        self._column_major_grid = bytearray()
        for i in range(self.ROW_LENGTH):
            self._column_major_grid.extend(self._grid[i :: self.ROW_LENGTH])

    def is_present(self, word: str) -> bool:
        if (
            len(self._column_major_grid) == 0
            or self._column_major_grid_row_length != self.ROW_LENGTH
        ):
            self._generate_column_major_grid()
        if len(word) > self.ROW_LENGTH:
            return False
        for current_grid in (self._grid, self._column_major_grid):
            current_index = 0
            while current_index < len(current_grid):
                found_index = current_grid.find(word.encode("ascii"), current_index)
                if found_index == -1:
                    break
                end_index = found_index + len(word) - 1
                if found_index // self.ROW_LENGTH == end_index // self.ROW_LENGTH:
                    return True
                current_index = found_index + 1
        return False
