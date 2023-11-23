from datetime import datetime, timezone, timedelta
import bcrypt
import jwt

from db import *

jwt_secret = "secret"
jwt_exp = 4 # hours

def authenticate_user(username: str, password: str):
    users = get_user_accounts()
    for user in users:
        if user.username == username and verify_password(password, user.passphrase):
            return generate_token(user.id)
    return False

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(user_id):
    token_json = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=jwt_exp),
        "user_id": user_id
    }
    return jwt.encode(token_json, jwt_secret, algorithm="HS256")

def verify_token(user_token):
    try:
        token = jwt.decode(user_token, jwt_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    users = get_user_accounts()
    for user in users:
        if(str(user.id) == token.get("user_id")):
            return user.id
    return False