import asyncio
from core.system import ActorSystem
from core.supervisor import Supervisor
from actors.echo import EchoActor
from core.messages import UserUtterance

async def main():
    system = ActorSystem()
    print(f"system {system}")
    echo = EchoActor(name="echo", system=system)
    print(f"echo {echo}")
    system.register(echo)
    tasks = await system.start_all()
    print(f"tasks {tasks}")

    factories = {
        "echo": lambda: EchoActor(name="echo", system=system)
    }

    supervisor = Supervisor()
    supervisor_task = asyncio.create_task(
        supervisor.watch(system, tasks, factories)
    )

    await system.tell("echo", UserUtterance(text="упади", timestamp=0.0))
    await asyncio.sleep(0.5)
    await system.tell("echo", UserUtterance(text="Привет", timestamp=0.0))
    await asyncio.sleep(0.5)

    await system.stop_all()
    supervisor_task.cancel()

asyncio.run(main())