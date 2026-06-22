import asyncio
from core.messages import ShutdownCommand

class Actor():
    def __init__(self, name):
        self.name = name
        self.inbox = asyncio.Queue()
        self._running = False

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._run())
        return self._task

    async def stop(self):
        self._running = False
        await self.inbox.put(ShutdownCommand)

    async def _run(self):
        while self._running:
            msg = await self.inbox.get()
            if isinstance(msg, ShutdownCommand):
                break
            else:
                try:
                    await self.receive(msg)
                except Exception as e:
                    print(f"Актор {self.name} упал: {e}")
                    raise

    async def receive(self, message):
        pass