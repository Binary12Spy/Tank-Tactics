import os
import bcrypt
import jwt
import urllib.request
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

import API.db as db

# Load the environment variables
load_dotenv()
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_EXPIRES_IN = os.environ.get("JWT_EXPIRES_IN") # In hours

#region Account Authentication
def authenticate_user(username: str, password: str):
    users = db.get_user_accounts()
    for user in users:
        if user.username == username and verify_password(password, user.hashed_password):
            return generate_token(user.id)
    return False

def verify_token(user_token):
    try:
        token = jwt.decode(user_token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    return token.get("user_id")
#endregion

#region Google ID Token Authentication
def authenticate_google_id_token(credential: str):
    try:
        _ = id_token.verify_oauth2_token(credential, requests.Request())
    except ValueError:
        return False
    return True

def get_google_user_info(credential: str):
    try:
        idinfo = id_token.verify_oauth2_token(credential, requests.Request())
    except ValueError as e:
        return e
    return idinfo

def hash_google_id(credential: str):
    return bcrypt.hashpw(credential.encode('utf-8'), bcrypt.gensalt())

def verify_hashed_google_id(credential: str, hashed_credential: str):
    return bcrypt.checkpw(credential.encode('utf-8'), hashed_credential.encode('utf-8'))
#endregion

#region Helper Functions
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(user_id):
    token_json = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=int(JWT_EXPIRES_IN)),
        "user_id": user_id
    }
    return jwt.encode(token_json, JWT_SECRET, algorithm="HS256")

def get_gid_jwk():
    return urllib.request.urlopen("https://www.googleapis.com/oauth2/v3/certs").read()
#endregion