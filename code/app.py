from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

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
  @jwt_required()
  def get(self, name):
    item = next(filter(lambda item: item['name'] == name, items), None)
    return {'item': item}, 200 if item else 404
  
  def post(self, name):
    request_data = request.get_json()
    if next(filter(lambda item: item['name'] == name, items), None):
      return {'message': 'An item with name {} already exist.'.format(name)}, 404
    
    new_item = {
      'name': name,
      'price': request_data['price']
    }
    items.append(new_item)
    return new_item, 201
  
  def delete(self, name):
    item = next(filter(lambda item: item['name'] == name, items), None)
    if item:
      items.remove(item)
      return {'message': f'{name} deleted successfully.'}, 200
    return {'message': f'item {name} does not exists in the database. delete failed.'}, 400
  
  def put(self, name):
    data = request.get_json()
    new = {'name': name, 'price': data['price']}
    item = next(filter(lambda item: item['name'] == name, items), None)
    if item:
      item['price'] = data['price']
      return item, 201
    else:
      items.append(new)
      return new, 201
  
class ItemList(Resource):
  @jwt_required()
  def get(self):
    return {'items': items}
  
  def post(self):
    items_list = request.get_json()
    if items_list:
      for item in items_list:
        items.append(item)
      return items_list, 200
    return {'item': None}, 400      

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)