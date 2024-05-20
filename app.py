import sys
import requests
from pi import pi


class app:
    def __init__(self) -> None:
        self.pi = pi()
        self.apiUrl = "http://localhost:9001"

        while True:
            self.waitingQRInput()

    def waitingQRInput(self):
        code = sys.stdin.readline().strip()

        if self.checkAccess(code):
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
    app()
