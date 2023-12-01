import os
import uvicorn
from typing import Optional
from fastapi import FastAPI, Response, Request, WebSocket
from pydantic import BaseModel
from dotenv import load_dotenv

from API.useraccounts import *
from API.game import *

app = FastAPI()
game_keeper = GameKeeper()

#Load Environment Variables
load_dotenv()
SERVER_PORT = os.environ.get("SERVER_PORT")
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

#region FastAPI Data Models
class Credentials(BaseModel):
    username: str
    password: str

class UserAccount(BaseModel):
    id: Optional[str]
    username: Optional[str]
    password: Optional[str]
    color_primary: Optional[str]
    color_secondary: Optional[str]
    is_admin: Optional[bool]
    
class PlayerProfile(BaseModel):
    id: Optional[str]
    health: Optional[int]
    action_tokens: Optional[int]
    range: Optional[int]
    is_alive: Optional[bool]
    has_voted: Optional[bool]
    received_votes: Optional[int]
    location_x: Optional[int]
    location_y: Optional[int]
#endregion

#region UserAccount Endpoints
@app.post("/register", tags=["Authentication"])
def register(user: Credentials, response: Response):
    result = register_user_account(user.username, user.password)
    if not result:
        return False
    token = generate_token(result.id)
    response.set_cookie(key="token", value=token)
    return True

@app.post("/authenticate", tags=["Authentication"])
def authenticate(credentials: Credentials, response: Response):
    token = authenticate_user(credentials.username, credentials.password)
    if not token:
        return False
    response.set_cookie(key="token", value=token)
    return True

@app.get("/user", tags=["Account"])
def get_user(request: Request):
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id:
        return False
    user_account = get_user_account(user_id)
    return user_account

@app.patch("/user", tags=["Account"])
def update_user(request: Request, updated_user: UserAccount):
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id:
        return False
    update_user_account(user_id, updated_user)
    return get_user_account(user_id)
#endregion

#region Game Management Endpoints
@app.post("/create-game", tags=["Game Management"])
def create_game(request: Request):
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id:
        return False
    game_id = game_keeper.create_game(user_id)
    return game_id

@app.post("/join-game/{lobby_id}", tags=["Game Management"])
def join_game(request: Request, lobby_id: str):
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id:
        return False
    game_keeper.join_game(user_id, lobby_id)
#endregion

#region Admin Endpoints
@app.delete("/game/{game_id}", tags=["Game Management", "Admin"])
def delete_game(request: Request, game_id: str):
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id:
        return False
    success = game_keeper.delete_game(user_id, game_id)
    return success

@app.post("/start-game/{game_id}", tags=["Game Management"])
def start_game(request: Request, game_id: str):
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id:
        return False
    success = game_keeper.start_game(user_id, game_id)
    return success
#endregion

#region Game Websocket Endpoint
@app.websocket("/game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    user_id = verify_token(str(websocket.cookies.get("token")))
    if not user_id:
        await websocket.close()
        return
    player_id = game_keeper.player_id_from_game_id(user_id, game_id)
    await game_keeper.connect(websocket, player_id)
    try:
        while True:
            data = await websocket.receive_text()
            if not verify_token(str(websocket.cookies.get("token"))):
                await websocket.send(False)
                await game_keeper.disconnect(player_id)
                return
            await game_keeper.handle_message(player_id, data)
    except:
        await game_keeper.disconnect(player_id)
#endregion

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=int(SERVER_PORT), reload=DEBUG)