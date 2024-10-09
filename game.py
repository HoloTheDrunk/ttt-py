import sys
from typing import Optional

from board import Board, Cell
from logger import Logger

class Game:
    win_req: int
    turn: Cell
    board: Board
    cursor: tuple[int, int]

    def __init__(self, /, win_req: int = 3, board_shape: Optional[list[list[bool]]] = None) -> None:
        self.board = Board() if board_shape is None else Board(board_shape)
        self.win_req = win_req
        self.turn = Cell.CROSS
        self.cursor = (0, 0)

    def run(self) -> None:
        print("\n".join(["h/j/k/l: ↑/↓/←/→", "space: place", "q: quit", "-------"]))

        win: int = -1

        while win == -1:
            if self.board.is_full():
                break
            
            selected: bool = False
            while not selected:
                ui = self.ui([f"Player {int(self.turn) + 1}'s ({self.turn}) turn."])
                print(ui + f'\033[{len(ui.splitlines()) - 1}F', end="")
                
                x, y = self.cursor

                try:
                    match sys.stdin.read(1):
                        case 'h':
                            x, y = (max(0, x - 1), y)
                        case 'j':
                            x, y = (x, min(y + 1, self.board.height() - 1))
                        case 'k':
                            x, y = (x, max(0, y - 1))
                        case 'l':
                            x, y = (min(x + 1, self.board.width() - 1), y)
                        case 'q':
                            raise KeyboardInterrupt()
                        case ' ':
                            selected = True
                        case _:
                            continue
                except KeyboardInterrupt as e:
                    print('\n' * len(ui.splitlines()), end='')
                    raise e
                
                if self.board.get(x, y) != Cell.BLOCK:
                    self.cursor = (x, y)
            
            if self.play(*self.cursor):
                if self.check_win():
                    win = self.turn
                else:
                    self.turn = Cell(1 - self.turn)

        print(self.ui(["Game finished."]), end=" ")
        
        if win == -1:
            print("It's a tie...")
        else:
            print(f"Player {int(self.turn) + 1} ({self.turn}) wins!")
        

    def play(self, x: int, y: int) -> bool:
        if self.board.get(x, y) != Cell.EMPTY:
            return False

        self.board.set(x, y, self.turn)
        return True

    def check_win(self) -> bool:
        offset_cursor = lambda t: (self.cursor[0] + dir[0] * t, self.cursor[1] + dir[1] * t)

        for dir in [(0, 1), (1, 1), (1, 0), (1, -1)]:
            start: int = 0
            end: int = 0

            for i in range(self.win_req):
                offset = offset_cursor(-i)

                if not self.board.contains(*offset):
                    break
                if self.board.get(*offset) != self.turn:
                    break

                start -= 1

            for i in range(self.win_req):
                offset = offset_cursor(i)

                if not self.board.contains(*offset):
                    break
                if self.board.get(*offset) != self.turn:
                    break

                end += 1

            if end - start == self.win_req + 1:
                return True

            # for i in range(self.win_req - 1):
            #     cell = self.board.get(*offset(i))
            #     Logger.log(f"Checking offset {self.cursor} + {dir} * {i}: '{cell}'") 
            #     if cell != self.turn:
            #         break
            # else:
            #     return True

        return False

    def ui(self, additional_lines: list[str] = []) -> str:
        lines = [
            *str(self.board).splitlines(),
            *additional_lines,
        ]

        x, y = self.cursor

        # Highlight cell under cursor
        # TODO: test if I can just jump and highlight (i.e. if CSI seq overwrite text)
        xOff = 2 * x + 1 # +1 for border, *2 for space between cells
        lines[y] = lines[y][:xOff] + '\033[7m' + lines[y][xOff] + '\033[0m' + lines[y][xOff + 1:]

        return "\n".join(lines)
