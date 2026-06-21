import asyncio
from actors.echo import EchoActor

async def main():
    echo = EchoActor(name="echo")
    await echo.start()
    await echo.inbox.put("Привет")
    await echo.inbox.put("еще одно сообение")
    await asyncio.sleep(0.1)
    await echo.stop()

asyncio.run(main())