import asyncio
from dataclasses import dataclass, field
from fastapi import WebSocket


@dataclass(eq=False)
class SocialConnection:
    socket: WebSocket
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


class SocialConnections:
    def __init__(self):
        self.users = {}  # user_id: set[SocialConnection]

    async def connect(self, user_id, socket):
        await socket.accept()
        connection = SocialConnection(socket)
        self.users.setdefault(user_id, set()).add(connection)
        return connection

    def disconnect(self, user_id, connection):
        connections = self.users.get(user_id)
        if connections is None:
            return

        connections.discard(connection)
        if not connections:
            self.users.pop(user_id, None)

    def is_online(self, user_id):
        return bool(self.users.get(user_id))

    async def close(self, user_id, connection):
        self.disconnect(user_id, connection)
        try:
            await asyncio.wait_for(connection.socket.close(), timeout=1)
        except Exception:
            pass

    async def send(self, user_id, connection, event):
        try:
            async with connection.lock:
                await asyncio.wait_for(
                    connection.socket.send_json(event), timeout=3
                )
            return True
        except Exception:
            await self.close(user_id, connection)
            return False

    async def push(self, user_id, event):
        connections = tuple(self.users.get(user_id, ()))
        if connections:
            await asyncio.gather(*(
                self.send(user_id, connection, event)
                for connection in connections
            ))