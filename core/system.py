import asyncio
from typing import Optional, Any
from uuid import uuid4

class ActorSystem:
    def __init__(self) -> None:
        """
        Инициализация ядра системы акторов.
        """
        # РЕЕСТР АКТОРОВ
        self.actors: dict[str, Any] = {}

        # ФОНОВЫЕ ЗАДАЧИ
        self.tasks: dict[str, asyncio.Task[Any]] = {}

        # ЗАЛ ОЖИДАНИЯ ОТВЕТОВ (RPC-паттерн Ask)
        self.pending_asks: dict[str, asyncio.Future[Any]] = {}

    def register(self, actor):
        # станет местом, где проверяется: нет ли уже актора с таким именем, доступна ли нужная нода для размещения 
        self.actors[actor.name] = actor

    async def start_all(self):
        """
        Запускает фоновые задачи для всех зарегистрированных акторов 
        и возвращает словарь этих задач.
        """
        for actor in self.actors.values():
            task = await actor.start()
            self.tasks[actor.name] = task
        return self.tasks
    
    async def stop_all(self):
        """
        Останавливает фоновые задачи для всех зарегистрированных акторов 
        и возвращает словарь этих задач.
        """
        for actor in self.actors.values():
            await actor.stop()


    # отправить сообщение БЕЗ ожидания ответа 
    async def tell(self, actor_name, message):
        if actor_name not in self.actors:
            raise ValueError(f"Актор {actor_name} не зарегистрирован")
        actor = self.actors[actor_name]
        await actor.inbox.put(message)


    # отправить сообщение с ожиданием ответа
    async def ask(self, actor_name: str, message, timeout: float = 5.0):
        correlation_id = str(uuid4())
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        message.correlation_id = correlation_id
        self.pending_asks[correlation_id] = future
        try:
            await self.tell(actor_name, message)
            result = await asyncio.wait_for(future, timeout=timeout)
            return result
        finally:
            self.pending_asks.pop(correlation_id, None)


    def resolve(self, correlation_id: str, response):
        future = self.pending_asks.get(correlation_id)
        if future is not None:
            future.set_result(response)