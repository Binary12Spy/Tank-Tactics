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
        for connection in self.connections.values():
            await connection.send_text(message)