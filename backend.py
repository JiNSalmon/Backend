from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ต้องอยู่หลังจากการสร้างแอปพลิเคชัน Flask

app.config['MONGO_URI'] = 'mongodb+srv://pawaritset:TadJT1HZ8zbocZXA@cluster0.pqgseqa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
mongo = PyMongo(app)

@app.route('/products', methods=['GET'])
def get_products():
    products = mongo.db.products.find()
    output = []
    for product in products:
        output.append({'_id': str(product['_id']), 'name': product['name'], 'price': product['price']})
    return jsonify(output)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    name = data['name']
    price = data['price']
    product_id = mongo.db.products.insert({'name': name, 'price': price})
    new_product = mongo.db.products.find_one({'_id': product_id})
    return jsonify({'_id': str(new_product['_id']), 'name': new_product['name'], 'price': new_product['price']}), 201

if __name__ == '__main__':
    app.run(debug=True)
