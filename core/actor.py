import asyncio
from messages import ShutdownCommand

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
                await self.receive(msg)

    async def receive(self, message):
        pass