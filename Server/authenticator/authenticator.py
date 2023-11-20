import bcrypt
from pydantic import BaseModel
from typing import List
from uuid import uuid4

from db import *

def authenticate_user(username: str, password: str):
    users = get_user_accounts()
    for user in users:
        if user.username == username and bcrypt.checkpw(password.encode('utf-8'), user.passphrase):
            return generate_token(user.id)
        
    return False

def register_user(username: str, password: str):
    users = get_user_accounts()
    for user in users:
        if user.username == username:
            return False

    user_id = str(uuid4())
    hashed_password = hash_password(password)
    token = generate_token(user_id)
    create_user_account(username, hashed_password, user_id, token)
    return token

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def generate_token(user_id):
    # generate token
    user_token = str(uuid4())

    users = get_user_accounts()
    for user in users:
        if( user.id == user_id):
            user.token = user_token
            update_user_account(user)
    return user_token

def verify_token(user_token):
    users = get_user_accounts()
    for user in users:
        if(str(user.token) == user_token):
            return True
    return False