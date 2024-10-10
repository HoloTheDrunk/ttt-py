from typing import Optional, Self
from enum import IntEnum

class Cell(IntEnum):
    BLOCK = -2
    EMPTY = -1
    CROSS = 0
    CIRCL = 1


    def __str__(self) -> str:
        match self:
            case Cell.BLOCK:
                return '░'
            case Cell.EMPTY:
                return ' '
            case Cell.CROSS:
                return 'X'
            case Cell.CIRCL:
                return 'O'


DEFAULT_BOARD: list[list[bool]] = [
    [True, True, False],
    [True, True, True],
    [True, True, True],
]

class Board:
    cells: list[list[Cell]]


    def __init__(
        self,
        board_shape: list[list[bool]] = DEFAULT_BOARD,
    ) -> None:
        height = len(board_shape)
        width = max(map(lambda row: len(row), board_shape))

        self.cells = [[
                Cell.EMPTY if board_shape[y][x] else Cell.BLOCK 
                for x in range(width)
            ] for y in range(height)]

    @classmethod
    def from_file(cls: type[Self], path: str) -> Self:
        with open(path) as file:
            true_char = file.readline()[0]
            board_shape = [[c == true_char for c in line.strip()] for line in file]
            return cls(board_shape)

    def size(self) -> tuple[int, int]:
        return (self.width(), self.height())
    

    def height(self) -> int:
        return len(self.cells)


    def width(self) -> int:
        return len(self.cells[0])

    
    def get(self, x: int, y: int) -> Cell:
        return self.cells[y][x]


    def set(self, x: int, y: int, v: Cell) -> None:
        self.cells[y][x] = v


    def contains(self, x: int, y: int) -> bool:
        return x >= 0 and y >= 0 \
            and x < self.width() and y < self.height()

    
    def safe_get(self, x: int, y: int) -> Optional[Cell]:
        if self.contains(x, y):
            return self.get(x, y)
        return None


    # PERF: could probably just count `set` calls
    def is_full(self) -> bool:
        for row in self.cells:
            for cell in row:
                if cell == Cell.EMPTY:
                    return False
        return True


    def clear(self) -> None:
        for row in self.cells:
            for i in range(len(row)):
                if row[i] > Cell.EMPTY:
                    row[i] = Cell.EMPTY


    def __str__(self) -> str:
        return "\n".join(
            '|' + 
                ' '.join(map(lambda c: str(c), self.cells[y]))
            + '|'
            for y in range(self.height()))
