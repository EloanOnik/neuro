import asyncio

class Supervisor():
    def __init__(self, restart_limit: int = 3, restart_window: float = 60.0):
        self.restart_limit = restart_limit
        self.restart_window = restart_window

    async def watch(self, system, tasks, factories):
        while True:
            done, pending = await asyncio.wait(
                tasks.values(),
                return_when=asyncio.FIRST_EXCEPTION
                )
            
            inverted_dict = {v: k for k, v in tasks.items()} # меняем ключи и значения местами
            for task in done:
                task_name = inverted_dict[task]

                new_actor = factories[task_name]()
                system.register(new_actor)
                new_task = await new_actor.start()
                tasks[task_name] = new_task
                print(f"restart actor {task_name} after a crash")
            
        