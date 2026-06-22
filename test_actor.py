import asyncio
from actors.echo import EchoActor
from core.system import ActorSystem
from core.messages import UserUtterance

async def main():
    system = ActorSystem()
    echo = EchoActor(name="echo", system=system)
    system.register(echo)
    await system.start_all()
    await system.tell("echo", UserUtterance(text="упади", timestamp=0.0))
    await asyncio.sleep(0.2)
    await system.tell("echo", UserUtterance(text="Привет", timestamp=0.0))
    await asyncio.sleep(0.2)
    await system.stop_all()



asyncio.run(main())