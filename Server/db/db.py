import random
from sqlmodel import Field, Session, SQLModel, create_engine

engine = create_engine("sqlite:///tank-tactics.db")

#region Database Models
class GameBoard(SQLModel, table=True):
    __tablename__ = "GameBoard"
    
    id: str = Field(default=None, primary_key=True)
    width: int = 30
    height: int = 30

class UserAccount(SQLModel, table=True):
    __tablename__ = "UserAccounts"
    
    id: str = Field(default=None, primary_key=True)
    username: str
    passphrase: str
    color_primary: str = "#" + hex(random.randrange(0, 2**24))[2:].upper()
    color_secondary: str = "#" + hex(random.randrange(0, 2**24))[2:].upper()
    admin: bool = False
    
class Player(SQLModel, table=True):
    __tablename__ = "Players"
    
    id: str = Field(default=None, primary_key=True)
    location_x: int
    location_y: int
    health: int = 3
    action_tokens: int = 1
    range: int = 1
    is_alive: bool = True
    has_voted: bool = False
    received_votes: int = 0
    
class EventLog(SQLModel, table=True):
    __tablename__ = "EventLog"
    
    id: str = Field(default=None, primary_key=True)
    player_id: str
    action: str
    target_id: str = Field(default=None, nullable=True)
    target_location: str = Field(default=None, nullable=True)
    timestamp: int
#endregion

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#region GameBoard Functions
def get_board_dimensions():
    with Session(engine) as session:
        board = session.get(GameBoard, "1")
        return (board.width, board.height)
#endregion

#region User Account Functions
def get_user_account_by_id(id: str):
    with Session(engine) as session:
        user_account = session.get(UserAccount, id)
        return user_account

def get_user_accounts():
    with Session(engine) as session:
        user_accounts = session.query(UserAccount).all()
        return user_accounts

def create_user_account(username: str, passphrase: str, id: str):
    with Session(engine) as session:
        user_account = UserAccount(username=username, passphrase=passphrase, id=id)
        session.add(user_account)
        session.commit()
        session.refresh(user_account)
        return user_account

def patch_user_account(user_account: UserAccount):
    with Session(engine) as session:
        session.merge(user_account)
        session.commit()
        return user_account
#endregion

#region Player Functions
def get_player(id: str):
    with Session(engine) as session:
        player = session.get(Player, id)
        return player
    
def get_players():
    with Session(engine) as session:
        players = session.query(Player).all()
        return players
    
def create_player(id: str, x: int, y: int):
    with Session(engine) as session:
        player = Player(id=id, x=x, y=y)
        session.add(player)
        session.commit()
        session.refresh(player)
        return player
    
def patch_player(player: Player):
    with Session(engine) as session:
        session.merge(player)
        session.commit()
        return player
    
def get_player_at_coordinates(x: int, y: int):
    with Session(engine) as session:
        player = session.query(Player).filter(Player.location_x == x).filter(Player.location_y == y).first()
        return player
#endregion

# Create the database and tables if they don't already exist
try:
    create_db_and_tables()
except:
    pass