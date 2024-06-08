from werkzeug.security import safe_str_cmp
from user import User

def authenticate(username, password):
  user = User.find_by_user_name(username)
  if user and safe_str_cmp(user.password, password):
    return user
  return None

def identity(payload):
  user_id = payload['identity']
  return User.find_by_id(user_id)
