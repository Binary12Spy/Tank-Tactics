from enum import Enum
from typing import Optional
from pydantic import BaseModel

from db import *

#region Models
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
#endregion

async def HandleAction(user_id, message: ActionModel):
    match message.action:
        case Action.MOVE:
            return HandleMove(user_id, message)
        case Action.ATTACK:
            return HandleAttack(user_id, message)
        case Action.UPGRADE:
            return HandleUpgrade(user_id, message)
        case Action.DONATE:
            return HandleDonate(user_id, message)
        case Action.VOTE:
            return HandleVote(user_id, message)

#region Action Handlers      
def HandleMove(user_id, message: ActionModel):
    return True

def HandleAttack(user_id, message: ActionModel):
    return True

def HandleUpgrade(user_id, message: ActionModel):
    return True

def HandleDonate(user_id, message: ActionModel):
    return True

def HandleVote(user_id, message: ActionModel):
    return True
#endregion