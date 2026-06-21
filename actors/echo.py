from core.actor import Actor

class EchoActor(Actor):
    async def receive(self, message):
        print(f"{self.name} получил: {message}")