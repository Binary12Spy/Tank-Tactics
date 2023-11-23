from game.connectionmanager import ConnectionManager

class GameKeeper:
    def __init__(self):
        self.connection_manager = ConnectionManager()
        
    async def connect(self, websocket, user_id):
        await self.connection_manager.disconnect(user_id)
        await self.connection_manager.connect(websocket, user_id)
        
    async def disconnect(self, user_id):
        await self.connection_manager.disconnect(user_id)
        
    async def handle_message(self, websocket, data):
        await self.connection_manager.broadcast(data)