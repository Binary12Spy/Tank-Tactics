import random
from sqlmodel import Field, Session, SQLModel, create_engine

engine = create_engine("sqlite:///tank-tactics.db")
session = Session(engine)

class UserAccount(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    username: str
    passphrase: str
    color_primary: str = "#" + hex(random.randrange(0, 2**24))[2:].upper()
    color_secondary: str = "#" + hex(random.randrange(0, 2**24))[2:].upper()
    admin: bool = False
    
class Player(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    x: int
    y: int
    health: int = 3
    action_tokens: int = 1
    range: int = 1
    is_alive: bool = True
    has_voted: bool = False
    received_votes: int = 0
    
class Log(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    player_id: str
    action: str
    target_id: str = Field(default=None, nullable=True)
    timestamp: int
    
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
        
def get_user_account(username: str):
    return session.get(UserAccount, username)

def get_user_account_by_id(id: str):
    user_account = session.get(UserAccount, id)
    return user_account

def get_user_accounts():
    user_accounts = session.query(UserAccount).all()
    return user_accounts

def create_user_account(username: str, passphrase: str, id: str):
    user_account = UserAccount(username=username, passphrase=passphrase, id=id)
    session.add(user_account)
    session.commit()
    session.refresh(user_account)
    return user_account

def patch_user_account(user_account: UserAccount):
    session.merge(user_account)
    session.commit()
    session.refresh(user_account)
    return user_account

def get_player(id: str):
    return session.get(Player, id)

def get_players():
    return session.query(Player).all()

def create_player(x: int, y: int):
    player = Player(x=x, y=y)
    session.add(player)
    session.commit()
    session.refresh(player)
    return player

def update_player(player: Player):
    session.add(player)
    session.commit()
    session.refresh(player)
    return player

def delete_player(player: Player):
    session.delete(player)
    session.commit()
    return True

def delete_all_players():
    session.query(Player).delete()
    session.commit()
    return True

def delete_user_account(user_account: UserAccount):
    session.delete(user_account)
    session.commit()
    return True

def delete_all_user_accounts():
    session.query(UserAccount).delete()
    session.commit()
    return True

def delete_all():
    delete_all_players(session)
    delete_all_user_accounts(session)
    return True

try:
    create_db_and_tables()
except:
    pass