from ast import List
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel

from authenticator import authenticate_user, register_user, verify_token

app = FastAPI()

class UserCredentials(BaseModel):
    username: str
    password: str
    
class Location(BaseModel):
    x: int
    y: int

class PlayerAction(BaseModel):
    action: str
    target: Location
    recipient_player_id: str

@app.post("/register")
def register(user: UserCredentials, response: Response):
    token = register_user(user.username, user.password)
    if not token:
        return False
    response.set_cookie(key="token", value=token)
    return True

@app.post("/authenticate")
def authenticate(credentials: UserCredentials, response: Response):
    token = authenticate_user(credentials.username, credentials.password)
    if not token:
        return False
    response.set_cookie(key="token", value=token)
    return True

@app.post("/player/action")
def player_action(action: PlayerAction):
    # Add your logic to handle the player action here
    action = action.action

    # Example action handling logic
    if action == "move":
        return {"message": "Player moved"}
    elif action == "shoot":
        return {"message": "Player shot"}
    else:
        return {"message": "Invalid action"}
   
@app.get("/board")
def get_board(request: Request):
    if not verify_token(str(request.cookies.get("token"))):
        return False
    # Add your logic to retrieve the board data here
    board_data = {"board": "Sample board data"}
    return board_data