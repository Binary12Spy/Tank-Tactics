import API.db as db
from API.game.connectionmanager import ConnectionManager
from API.game import actionlogic
from API.game.actionlogic import ActionModel

class GameKeeper:
    def __init__(self):
        self.connection_manager = ConnectionManager()
    
#region Connection Manager
    async def connect(self, websocket, player_id):
        await self.connection_manager.disconnect(player_id)
        await self.connection_manager.connect(websocket, player_id)
        
    async def disconnect(self, user_id):
        await self.connection_manager.disconnect(user_id)
#endregion

#region Player Management
#endregion

#region Game Helper Functions
#endregion

#region Game Logic
    async def broadcast_game_state(game_id, self):
        players = db.get_players_in_game(game_id)
        await self.connection_manager.broadcast(players, "{\"type\": \"game_state\", \"data\": \"test\"}")

    async def handle_message(self, user_id, data):
        try:
            action = ActionModel.parse_raw(data)
        except:
            await self.connection_manager.send_personal_message("error", user_id)
            await self.connection_manager.disconnect(user_id)
            return
        result = await actionlogic.HandleAction(user_id, action)
        
        if not result:
            await self.connection_manager.send_personal_message("error", user_id)
        else:
            await self.broadcast_game_state()
#endregion

#regioan Helper Functions
    def player_id_from_game_id(self, user_id, game_id):
        return db.get_player_id_from_game_id(user_id, game_id)