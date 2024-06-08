from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
import sqlite3

from user import UserRegister

app = Flask(__name__)
app.secret_key = "random_cfg"
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = [
  {
    'name': 'chair', 'price': 100
  }
]

class Item(Resource):
  # @jwt_required()
  def get(self, name):
    query = """
      SELECT * FROM item WHERE name=?
    """
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    result = cursor.execute(query, (name,))#.fetchone()
    if result:
      vals = []
      for item in result:
        vals.append({'name': item[1], 'price': item[2]})
      return {'vals': vals}, 200 if result else 404
    conn.close()
  
  # @jwt_required()
  def post(self, name):
    request_data = request.get_json()
    fetch_query = """
      SELECT * FROM item WHERE name=?
    """
    
    post_query = """
      INSERT INTO item VALUES (NULL, ?, ?)
    """
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    result = cursor.execute(fetch_query, (name,)).fetchone()
    if result:
      return {'message': 'An item with name {} already exist.'.format(name)}, 404
  
    cursor.execute(post_query, (name, request_data['price']))
    
    conn.commit()
    conn.close()
    
    return {
      'name': name,
      'price': request_data['price']
    }, 201
  
  # @jwt_required()
  def delete(self, name):
    item = next(filter(lambda item: item['name'] == name, items), None)
    if item:
      items.remove(item)
      return {'message': f'{name} deleted successfully.'}, 200
    return {'message': f'item {name} does not exists in the database. delete failed.'}, 400
  
  # @jwt_required()
  def put(self, name):
    data = request.get_json()
    new = {'name': name, 'price': data['price']}
    item = next(filter(lambda item: item['name'] == name, items), None)
    if item:
      item['price'] = data['price']
      item['name'] = data['name'] if data['name'] else item['name']
      return item, 201
    else:
      items.append(new)
      return new, 201
  
class ItemList(Resource):
  # @jwt_required()
  def get(self):
    query = """
      SELECT * FROM item
    """
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    result = cursor.execute(query).fetchall()
    vals = []
    if result:
      for item in result:
        vals.append({'name': item[1], 'price': item[2]})
    conn.close()
    return {'data': vals}, 200 if result else 404
  
  # @jwt_required()
  def post(self):
    items_list = request.get_json()
    vals = []
    if items_list:
      for item in items_list:
        vals.append((item['name'], item['price']))
      
      conn = sqlite3.connect('data.db')
      cursor = conn.cursor()
      
      insert_query = """
        INSERT INTO item VALUES (NULL, ?, ?)
      """
      cursor.executemany(insert_query, vals)
      conn.commit()
      conn.close()
      
    return {'data': vals}, 201 if vals else 400      

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register/<string:username>')

app.run(port=5000, debug=True)