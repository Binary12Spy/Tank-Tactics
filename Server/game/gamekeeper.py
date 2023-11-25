import random

import db
from game.connectionmanager import ConnectionManager
from game import actionlogic
from game.actionlogic import ActionModel

class GameKeeper:
    def __init__(self):
        self.connection_manager = ConnectionManager()
    
#region Connection Manager
    async def connect(self, websocket, user_id):
        await self.connection_manager.disconnect(user_id)
        await self.connection_manager.connect(websocket, user_id)
        
    async def disconnect(self, user_id):
        await self.connection_manager.disconnect(user_id)
#endregion

#region User Management
#endregion

#region Game Management
    async def place_players_on_board(self):
        # Get all user accounts from the database
        user_accounts = db.get_user_accounts()

        # Create player objects in the DB for each user
        for user_account in user_accounts:
            player = db.Player(user_id=user_account.user_id)
            await player.save()

        # Place players randomly on the board
        (board_width, board_height) = db.get_board_dimensions()
        players = db.get_players()
        for player in players:
            while True:
                x = random.randint(0, board_width - 1)
                y = random.randint(0, board_height - 1)
                # Check if the spot is already occupied by another player
                if not db.get_player_at_coordinates(x, y):
                    player.location_x = x
                    player.location_y = y
                    await player.save()
                    break
#endregion

#region Game Logic
    async def broadcast_game_state(self):
        await self.connection_manager.broadcast("{\"type\": \"game_state\", \"data\": \"test\"}")

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