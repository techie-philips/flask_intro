import sqlite3
from flask_restful import Resource, reqparse



class User:
  def __init__(self, _id, username, password):
    self.id = _id
    self.username = username
    self.password = password
    
  @classmethod
  def find_by_user_name(cls, username):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    query = """
      SELECT id, username, password FROM user WHERE username=?
    """
    result = cursor.execute(query, (username,))
    user_info = result.fetchone()
    if user_info:
      # print("user exists!!")
      user = cls(*user_info)
    else:
      user = None
      
    cursor.close()
    return user
  
  @classmethod
  def find_by_id(cls, id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    query = """
      SELECT id, username, password FROM user WHERE id=?
    """
    result = cursor.execute(query, (id,))
    row = result.fetchone()
    
    if row:
      user = cls(*row)
    else:
      user = None
      
    cursor.close()
    return user
  
class UserRegister(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument(
    'username', type=str, required=True, help="This field cannot be blank."
  )
  parser.add_argument(
    'password', type=str, required=True, help="This field cannot be blank."
  )
  
  @classmethod
  def post(cls, username):
    data = cls.parser.parse_args()
    
    user = User.find_by_user_name(data['username'])
    if user:
      return {'message': 'User with username {} already exists'.format(data['username'])}, 400
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    insert_user_query = """
      INSERT INTO user VALUES (NULL, ?, ?)
    """
    cursor.execute(insert_user_query, (data['username'], data['password']))
    
    conn.commit()
    conn.close()
    
    return {
      'data': {'username': data['username'], 'password': data['password']
      }, 'message': 'User created successfully'}, 201