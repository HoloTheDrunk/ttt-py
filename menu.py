from time import sleep
import sys
import os

from logger import Logger
from board import Board
from game import Game
from utils import send

class Menu:
    boards: list[tuple[str, Board]]
    longest_name: int
    dim: tuple[int, int]
    cursor: int
    scroll: int


    def __init__(self, directory: str = "boards", dim: tuple[int, int] = (80, 5)) -> None:
        self.boards = []
        for file in os.listdir(directory):
            if file[-4:] != '.ttt':
                continue
            self.boards.append((file, Board.from_file(f'{directory}/{file}')))
        self.boards.sort(key=lambda tup: tup[0])

        self.longest_name = max(map(lambda board: len(board[0]), self.boards))
        self.dim = dim
        self.cursor = 0
        self.scroll = 0


    def run(self) -> None:
        instructions = ["j/k: ↓/↑", "space: select", "q: quit", "-------"]
        print("\n".join(instructions))

        picked = -1

        while picked == -1:
            list_view = self.list_view()
            
            Logger.log(list_view)

            send(list_view)

            send(f"\033[{self.dim[1] - 1}A\033[0G")

            board = self.boards[self.scroll + self.cursor][1];
            board_lines = str(board).splitlines()
            for i in range(self.dim[1]):
                # Cleanup line
                send(f'\033[{self.longest_name + 5}C\033[K')

                if i < board.height():
                    # Print board line
                    send(board_lines[i][:self.dim[0]])
                
                # Go to the next line
                send("\033[E")

            # Go back up
            send(f'\033[{self.dim[1]}F')

            sys.stdout.flush()

            while True:
                try:
                    match sys.stdin.read(1):
                        case 'j': self.cursor_down()
                        case 'k': self.cursor_up()
                        case ' ': picked = self.scroll + self.cursor
                        case 'q': raise KeyboardInterrupt
                        case _: continue
                except KeyboardInterrupt as e:
                    send(f'\033[{min(self.dim[1], max(len(self.boards), board.height()))}E')
                    raise e
                break

        if picked != -1:
            true_height = len(instructions) + self.dim[1]
            board = self.boards[picked][1]
            send('\033[2K\033[E' * true_height + f'\033[{true_height}F')
            Game(board=board).run()


    def cursor_up(self) -> None:
        if self.scroll + self.cursor == 0:
            return

        if self.cursor == 1 and self.scroll > 0:
            self.scroll -= 1
        else:
            self.cursor -= 1


    def cursor_down(self) -> None:
        if self.scroll + self.cursor == len(self.boards) - 1:
            return

        if self.cursor == self.dim[1] - 1:
            self.scroll += 1
        else:
            self.cursor += 1


    def list_view(self) -> str:
        _, height = self.dim
        current = self.scroll + self.cursor

        list_view = [ ]
        for (i, (name, _)) in enumerate(self.boards[self.scroll : height + self.scroll]):
            if i == current:
                list_view.append(f'\033[1;7m> {name}\033[0m{" " * (self.longest_name - len(name))} |')
            else:
                list_view.append(f'{name}{" " * (self.longest_name - len(name) + 2)} |')

        if len(list_view) < height:
            list_view.extend([''] * (height - len(list_view)))

        return "\n".join(list_view)
