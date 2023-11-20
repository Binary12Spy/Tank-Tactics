from ast import List
from typing import Optional
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel

from authenticator import authenticate_user, register_user, verify_token, hash_password
from db import *

app = FastAPI()

class UserCredentials(BaseModel):
    username: str
    password: str

class PlayerAction(BaseModel):
    action: str
    target_x: int
    target_y: int
    recipient_player_id: str
    
class UpdatedUser(BaseModel):
    username: Optional[str]
    password: Optional[str]
    primary_color: Optional[str]
    secondary_color: Optional[str]

@app.post("/register", tags=["Authentication"])
def register(user: UserCredentials, response: Response):
    token = register_user(user.username, user.password)
    if not token:
        return False
    response.set_cookie(key="token", value=token)
    return True

@app.post("/authenticate", tags=["Authentication"])
def authenticate(credentials: UserCredentials, response: Response):
    token = authenticate_user(credentials.username, credentials.password)
    if not token:
        return False
    response.set_cookie(key="token", value=token)
    return True

@app.get("/user", tags=["Account"])
def get_user(request: Request):
    if not verify_token(str(request.cookies.get("token"))):
        return False
    # Add your logic to retrieve the user account here
    user_account = get_user_account_by_token(str(request.cookies.get("token")))
    return {"username": user_account.username, "primary_color": user_account.color_primary, "secondary_color": user_account.color_secondary}

@app.patch("/user", tags=["Account"])
def update_user(request: Request, updated_user: UpdatedUser):
    if not verify_token(str(request.cookies.get("token"))):
        return False
    # Add your logic to update the user account here
    # You can access the updated user attributes using the `updated_user` parameter

    # Example update logic
    user = get_user_account_by_token(str(request.cookies.get("token")))
    if updated_user.password != None:
        updated_user.password = hash_password(updated_user.password)
    user.username = updated_user.username or user.username
    user.passphrase = updated_user.password or user.passphrase
    user.color_primary = updated_user.primary_color or user.color_primary
    user.color_secondary = updated_user.secondary_color or user.color_secondary
    update_user_account(user)
    
    return {"message": "User account updated successfully"}

@app.delete("/user", tags=["Account"])
def delete_user(request: Request):
    if not verify_token(str(request.cookies.get("token"))): return False
    # Add your logic to delete the user account here
    # You can access the user account using the token from the request cookies
    user_account = get_user_account_by_token(str(request.cookies.get("token")))
    delete_user_account(user_account)
    
    return {"message": "User account deleted successfully"}

@app.post("/player/action", tags=["Player"])
def player_action(request: Request, action: PlayerAction):
    if not verify_token(str(request.cookies.get("token"))): return False
    # Add your logic to handle the player action here
    action = action.action

    # Example action handling logic
    if action == "move":
        return {"message": "Player moved"}
    elif action == "shoot":
        return {"message": "Player shot"}
    else:
        return {"message": "Invalid action"}
   
@app.get("/board", tags=["Game"])
def get_board(request: Request):
    if not verify_token(str(request.cookies.get("token"))): return False
    # Add your logic to retrieve the board data here
    board_data = {"board": "Sample board data"}
    return board_data