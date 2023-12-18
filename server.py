import os
import uvicorn
import starlette.status as status
from typing import Optional
from fastapi import FastAPI, Form, Response, Request, WebSocket, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
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

@app.get("/")
def root(request: Request):
    if request.cookies.get("token") is None:
        response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        return response
    else:
        response = RedirectResponse(url="/game", status_code=status.HTTP_302_FOUND)
        return response

#region Authentication Endpoints
@app.post("/register", tags=["Authentication"])
def register(user: Credentials, response: Response):
    result = register_user_account(user.username, user.password)
    if not result:
        return False
    token = generate_token(result.id)
    response.set_cookie(key="tank-tactics_token", value=token)
    return True

@app.post("/authenticate", tags=["Authentication"])
def authenticate(credentials: Credentials, response: Response):
    token = authenticate_user(credentials.username, credentials.password)
    if not token:
        raise HTTPException(status_code=401, detail="Authentication failed")
    response.set_cookie(key="tank-tactics_token", value=token)
    return True

@app.post("/sign-in-with-google", tags=["Account"])
def gid_login(response: Response, credential: str = Form(...), g_csrf_token: str = Form(...)):
    if not authenticate_google_id_token(credential):
        raise HTTPException(status_code=401)
    google_account_info = get_google_user_info(credential)
    user_id = google_user_account(google_account_info)
    token = generate_token(user_id)
    response = RedirectResponse(url="/game", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="tank-tactics_token", value=token)
    return response
#endregion

#region Account Management Endpoints
@app.get("/user", tags=["Account"])
def get_user(request: Request):
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user_account = get_user_account(user_id)
    return user_account

@app.patch("/user", tags=["Account"])
def update_user(request: Request, updated_user: UserAccount):
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication failed")
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

#region Webserver Endpoints
app.mount("/static", StaticFiles(directory="UI"), name="static")

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse("UI/favicon.ico")

@app.get("/login")
async def get_login():
    return FileResponse("UI/Account/login.html")

@app.get("/register")
async def get_register():
    return FileResponse("UI/Account/register.html")

@app.get("/game")
async def get_game():
    return FileResponse("UI/Game/game.html")
#endregion

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=int(SERVER_PORT), reload=DEBUG)