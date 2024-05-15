from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
	{
		'name': 'Wonder Store',
		'items': [
			{
				'name': 'Shoe',
				'price': 67.98
			}
		]
	}
]

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/store', methods=['POST'])
def create_store():
	request_data = request.get_json()
	new_store = {
		'name': request_data['name'],
		'items': []
	}
	stores.append(new_store)
	return jsonify(new_store)

@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
	for store in stores:
		if store['name'] == name:
			return jsonify({'store': store})
	return jsonify({'status': 'failed', 'message': 'store not found'})


@app.route('/store')
def get_stores():
	if stores:
		message = 'found some stores!' 
	else:
		message = 'no store found'
	return jsonify({'stores': stores, 'message': message, 'status': 'successful'})

@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
	request_data = request.get_json()
	for store in stores:
		if store['name'] == name:
			new_item = {
				'name': request_data['name'],
				'price': request_data['price']
			}
			store['items'].append(new_item)
			return jsonify({'status': 'successful'})
	return jsonify({'status': 'failed'})

@app.route('/store/<string:name>/item')
def get_items_in_store(name):
	for store in stores:
		if store['name'] == name:
			return jsonify({'store items': store['items'], 'status': 'successful'})
	return jsonify({'status': 'failed', 'message': 'no store with that name'})

# app.run(port=5000, debug=True)