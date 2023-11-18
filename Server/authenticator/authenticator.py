import bcrypt
from pydantic import BaseModel
from typing import List
from uuid import uuid4

class User(BaseModel):
    username: str
    password: str
    user_id: str
    user_token: str

users: List[User] = []

def authenticate_user(username: str, password: str):
    for user in users:
        if user["username"] == username and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            return generate_token(user["user_id"])
    return False

def register_user(username: str, password: str):
    for user in users:
        if user["username"] == username:
            return False

    user_id = str(uuid4())
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    token = generate_token(user_id)
    users.append({
        "username": username,
        "password": hashed_password,
        "user_id": user_id,
        "user_token": token
    })
    return token

def generate_token(user_id):
    # generate token
    user_token = str(uuid4())

    for user in users:
        if( user["user_id"] == user_id):
            user["user_token"] = user_token
    return user_token

def verify_token(user_token):
    for user in users:
        if(str(user["user_token"]) == user_token):
            return True
    return False