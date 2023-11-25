import asyncio
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections = {}

#region Primary Connection Functions
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
#endregion

#region Message Sending Functions
    async def send_personal_message(self, message: str, player_id: int):
        await self.connections[player_id].send_text(message)
        
    async def broadcast(self, player_ids, message: str):
        async def send_message(connection):
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Failed to send message: {e}")
        await asyncio.gather(*[send_message(self.connections[player_id]) for player_id in player_ids])
#endregion