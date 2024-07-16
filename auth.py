import logging
import requests

apiUrl = "https://ams-api.dyhs.kr"


def checkAccess(code=None):
    logging.debug(f"Check Access: {code}")
    try:
        if code is None:
            res = requests.get(f"{apiUrl}/auth/access", timeout=5)
        else:
            res = requests.get(
                f"{apiUrl}/auth/access", params={"code": code}, timeout=5
            )

        if res.status_code != 200:
            return False

        data = res.json()
        return data["status"]
    except requests.exceptions.ReadTimeout:
        return True
