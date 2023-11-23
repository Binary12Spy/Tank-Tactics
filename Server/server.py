from typing import Optional
from fastapi import FastAPI, Response, Request, WebSocket
from pydantic import BaseModel

from authenticator import *
from useraccounts import *
from game import *

app = FastAPI()
game_keeper = GameKeeper()

class UserCredentials(BaseModel):
    username: str
    password: str

class UpdatedUser(BaseModel):
    username: Optional[str]
    password: Optional[str]
    color_primary: Optional[str]
    color_secondary: Optional[str]

#region REST API Endpoints
@app.post("/register", tags=["Authentication"])
def register(user: UserCredentials, response: Response):
    result = register_user_account(user.username, user.password)
    if not result:
        return False
    token = generate_token(result.id)
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
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id:
        return False
    user_account = get_user_account(user_id)
    return user_account

@app.patch("/user", tags=["Account"])
def update_user(request: Request, updated_user: UpdatedUser):
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id:
        return False
    update_user_account(user_id, updated_user)
    return get_user_account(user_id)
#endregion

#region Game Endpoints
@app.post("/game/start", tags=["Game"])
def start_game(request: Request):
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id:
        return False
    user = get_user_account(user_id)
    if not user.admin:
        return False
    game_keeper.place_players_on_board()
    return True

@app.websocket("/game")
async def websocket_endpoint(websocket: WebSocket):
    user_id = verify_token(str(websocket.cookies.get("token")))
    if not user_id:
        await websocket.close()
        return
    await game_keeper.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            if not verify_token(str(websocket.cookies.get("token"))):
                await websocket.send(False)
                await game_keeper.disconnect(user_id)
                return
            await game_keeper.handle_message(user_id, data)
    except:
        await game_keeper.disconnect(user_id)
#endregion