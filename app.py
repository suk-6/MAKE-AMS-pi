import sys
import tty
import termios
from pi import pi
import logging
from auth import checkAccess


logging.basicConfig(filename="./log.txt", level=logging.DEBUG)


def get_single_character():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


class app:
    def __init__(self) -> None:
        self.pi = pi()

        while True:
            self.waitingQRInput()

    def waitingQRInput(self):
        buffer = []

        while 1:
            char = get_single_character()
            if char == "(":
                buffer = []
            if char == "!":
                sys.exit()

            buffer.append(char)
            logging.debug(buffer)

            if char == ")":
                break

        if buffer[0] == "(" and buffer[-1] == ")":
            buffer.pop(0)
            buffer.pop(-1)
        else:
            return

        if checkAccess("".join(buffer)):
            self.pi.doorOpen()


if __name__ == "__main__":
    while 1:
        try:
            app()
        except Exception as e:
            print(e)
            pass
