from core.actor import Actor

class EchoActor(Actor):
    def __init__(self, name, system):
        super().__init__(name)
        self.system = system
    async def receive(self, message):
        if getattr(message, 'text', None) == "упади":
            raise RuntimeError("Тестовое падение")
        print(f"{self.name} получил: {message}")