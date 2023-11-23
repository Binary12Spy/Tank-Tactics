from uuid import uuid4

from db import *
from authenticator import *

def register_user_account(username, password):
    users = get_user_accounts()
    for user in users:
        if user.username == username:
            return False
    return create_user_account(username, hash_password(password), str(uuid4()))

def update_user_account(id, updated_user):
    user = get_user_account(id)
    if not user:
        return False
    user.username = updated_user.username
    if updated_user.password:
        user.passphrase = hash_password(updated_user.password)
    user.color_primary = updated_user.color_primary
    user.color_secondary = updated_user.color_secondary
    patch_user_account(user)
    return True

def delete_user_account(user):
    users = get_user_accounts()
    for u in users:
        if u.id == user.id:
            u.delete()
            return True
    return False

def get_user_account(user_id):
    user = get_user_account_id(user_id)
    if not user:
        return False
    return {"id": user.id, "username": user.username, "primary_color": user.color_primary, "secondary_color": user.color_secondary}