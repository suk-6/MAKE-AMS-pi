import sys
import tty
import termios
import requests
from pi import pi


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
        self.apiUrl = "https://ams-api.dyhs.kr"

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

            if char == ")":
                break

        if buffer[0] == "(" and buffer[-1] == ")":
            buffer.pop(0)
            buffer.pop(-1)
        else:
            return

        print(buffer)
        if self.checkAccess("".join(buffer)):
            self.pi.doorOpen()

    def checkAccess(self, code):
        try:
            res = requests.get(
                f"{self.apiUrl}/auth/access", params={"code": code}, timeout=5
            )
            if res.status_code != 200:
                return False

            data = res.json()
            return data["status"]
        except requests.exceptions.ReadTimeout:
            return True


if __name__ == "__main__":
    while 1:
        try:
            app()
        except Exception as e:
            print(e)
            pass
