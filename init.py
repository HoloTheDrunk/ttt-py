import sys
import tty
import termios

from logger import Logger
from game import Board, Game

def main():
    game = Game(board=Board.from_file("boards/big-x.ttt"))
    game.run()

if __name__ == "__main__":
    stdin = sys.stdin.fileno()
    old_settings = termios.tcgetattr(stdin)
    tty.setcbreak(sys.stdin)

    # Hide cursor
    print('\033[?25l', end="")

    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        try:
            Logger.log(f"Error: {e}")
        except Exception:
            # screw it, no error for you
            pass

    # Show cursor again
    print('\033[?25h', end="")

    termios.tcsetattr(stdin, termios.TCSADRAIN, old_settings)
