from typing import Optional
from fastapi import FastAPI, Response, Request, WebSocket
from pydantic import BaseModel

from useraccounts import *
from game import *

app = FastAPI()
game_keeper = GameKeeper()

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

#region Admin Endpoints
@app.get("/admin/user", tags=["Admin"])
def get_user(request: Request, id: str):
    print(str(request.cookies.get("token")))
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id or not is_admin(user_id):
        return False
    if not id:
        return False
    user_account = get_user_account(id)
    return user_account

@app.patch("/admin/user", tags=["Admin"])
def update_user(request: Request, updated_user: UserAccount):
    user_id = verify_token(str(request.cookies.get("token")))
    if not is_admin(user_id) or not user_id:
        return False
    patch_user_account(updated_user.id, updated_user)
    return get_user_account(updated_user.id)

@app.get("/admin/users", tags=["Admin"])
def get_users(request: Request):
    user_id = verify_token(str(request.cookies.get("token")))
    if not is_admin(user_id) or not user_id:
        return False
    users = get_user_accounts()
    return users

@app.delete("/user", tags=["Account"])
def delete_user(id: str, request: Request):
    user_id = verify_token(str(request.cookies.get("token")))
    if not user_id or not is_admin(user_id):
        return False
    delete_user_account(id)
    return True
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