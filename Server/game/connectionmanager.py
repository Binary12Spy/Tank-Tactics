import asyncio
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections = {}
        
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.connections[user_id] = websocket
        
    async def disconnect(self, user_id: int):
        if user_id in self.connections:
            try:
                await self.connections[user_id].close()
            except:
                pass
            del self.connections[user_id]
        
    async def send_personal_message(self, message: str, user_id: int):
        await self.connections[user_id].send_text(message)
        
    async def broadcast(self, message: str):
        async def send_message(connection):
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Failed to send message: {e}")

        await asyncio.gather(*(send_message(connection) for connection in self.connections.values()))