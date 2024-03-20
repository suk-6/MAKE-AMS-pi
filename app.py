import asyncio
from pi import pi


class app:
    def __init__(self) -> None:
        self.pi = pi()

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.waitingButtonInput())
        self.loop.run_forever()

    async def waitingButtonInput(self):
        while True:
            self.pi()
            await asyncio.sleep(0.001)


if __name__ == "__main__":
    app = app()
