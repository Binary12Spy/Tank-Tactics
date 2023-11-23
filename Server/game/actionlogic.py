from enum import Enum
from typing import Optional
from pydantic import BaseModel

from db import *

class Action(Enum):
    MOVE = "move"
    ATTACK = "attack"
    UPGRADE = "upgrade"
    DONATE = "donate"
    VOTE = "vote"

class ActionModel(BaseModel):
    action: Action
    target_x: Optional[int] = None
    target_y: Optional[int] = None
    target_id: Optional[str] = None

async def HandleAction(user_id, message: ActionModel):
    match message.action:
        case Action.MOVE:
            return HandleMove(user_id, message)
        case Action.ATTACK:
            return HandleAttack(user_id, message)
        # case Action.UPGRADE:
        #     return HandleUpgrade(user_id, message)
        # case Action.DONATE:
        #     return HandleDonate(user_id, message)
        # case Action.VOTE:
        #     return HandleVote(user_id, message)
            
def HandleMove(user_id, message: ActionModel):
    # Message needs target coordinates
    if not message.target_x or not message.target_y:
        return False
    
    # Check that the player is alive
    player = get_player(user_id)
    if not player.is_alive:
        return False
    
    # Check that the space is 1 tile away in the x or y direction
    if abs(player.location_x - message.target_x) > 1 or abs(player.location_y - message.target_y) > 1:
        return False
    
    # Check that the player has enough action tokens
    if player.action_tokens < 1:
        return False
    
    # Check that the target coordinates are not the player's current coordinates
    if player.location_x == message.target_x and player.location_y == message.target_y:
        return False
    
    # Check no player is at the target coordinates
    target_player = get_player_at_coordinates(message.target_x, message.target_y)
    if target_player:
        return False
    
    # Check that the target coordinates are within the map bounds
    (map_x, map_y) = get_board_dimensions()
    if message.target_x < 0 or message.target_x >= map_x or message.target_y < 0 or message.target_y >= map_y:
        return False
    
    # Update player coordinates and subtract action tokens
    player.location_x = message.target_x
    player.location_y = message.target_y
    player.action_tokens -= 1
    patch_player(player)

    return True

def HandleAttack(user_id, message: ActionModel):
    # Message needs target coordinates
    if not message.target_x or not message.target_y:
        return False
    
    # Check that the player is alive
    player = get_player(user_id)
    if not player.is_alive:
        return False
    
    # Check that the player has enough action tokens
    if player.action_tokens < 1:
        return False
    
    # Check that the target coordinates are not the player's current coordinates
    if player.location_x == message.target_x and player.location_y == message.target_y:
        return False
    
    # Check that the target coordinates are within the map bounds
    (map_x, map_y) = get_board_dimensions()
    if message.target_x < 0 or message.target_x >= map_x or message.target_y < 0 or message.target_y >= map_y:
        return False
    
    # Check that the target coordinates are occupied by a player
    target_player = get_player_at_coordinates(message.target_x, message.target_y)
    if not target_player:
        return False
    
    # Check that the target player is alive
    if not target_player.is_alive:
        return False
    
    # Check that the target player is not the player
    if target_player.id == player.id:
        return False
    
    # Check that the target player is within range
    if player.range < abs(player.location_x - target_player.location_x) or player.range < abs(player.location_y - target_player.location_y):
        return False
    
    # Update player coordinates and subtract action tokens
    player.action_tokens -= 1
    patch_player(player)
    
    # Update target player's health
    target_player.health -= 1
    if target_player.health <= 0:
        target_player.is_alive = False
    patch_player(target_player)

    return True