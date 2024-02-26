from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask,jsonify,request
from pymongo.mongo_client import MongoClient
from flask_basicauth import BasicAuth
import certifi

app = Flask(__name__)
CORS(app)
app.config['BASIC_AUTH_USERNAME'] = 'jvaeswby'
app.config['BASIC_AUTH_PASSWORD'] = 'de6b8491-7936-4f4c-a08a-444f4b3168c7'
basic_auth = BasicAuth(app)

ca = certifi.where()
uri = "mongodb+srv://admin:ByN34uzcW4U0KVK1@cluster0.0tekyfx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(uri, tlsCAFile=ca)
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/products', methods=['GET'])
def get_products():
    db = client["productDB"]
    products_collection =  db['products']  # เลือกคอลเลกชัน "products" จากฐานข้อมูล
    all_products = list(products_collection.find())
    return jsonify(all_products)


@app.route("/products", methods=["POST"])
def add_new_product():
    db = client["productDB"]
    products_collection =  db['products']
    data = request.get_json()
    new_product={
        "_id":data["_id"],
        "name": data["name"],
        "price": data["price"],
        "description": data["description"]
    }
    all_products = list(products_collection.find())
    if(next((s for s in all_products if s["_id"] == data["_id"]), None)):
        return jsonify( {"error":"Cannot create new student"}),500
    else:
        products_collection.insert_one(new_product)
        return jsonify(new_product),200

@app.route("/products/<string:_id>", methods=["DELETE"])
def delete_student(_id):
    db = client["productDB"]
    products_collection =  db['products']
    all_products = list(products_collection.find())
    if(next((s for s in all_products if s["_id"] == _id), None)):
        products_collection.delete_one({"_id":_id})
        return jsonify({"message":"Student deleted successfully"}),200
    else:
        return jsonify({"error":"Student not found"}),404

@app.route("/products/<string:_id>", methods=["PUT"])
def update_product(_id):
    db = client["productDB"]
    products_collection = db['products']
    
    # Extract JSON data from the request body
    data = request.get_json()

    # Update fields for the product with the given _id
    update_data = {
        "name": data["name"],
        "price": data["price"],
        "description": data["description"]
    }

    # Perform the update operation
    result = products_collection.update_one(
        {"_id": _id},  # Match the product with the given _id
        {"$set": update_data}  # Set the new values
    )

    # Check if the product was found and updated
    if result.modified_count > 0:
        updated_product = products_collection.find_one({"_id": _id})
        return jsonify(updated_product), 200
    else:
        return jsonify({"error": "Product not found or no changes were made"}), 404 
      
if __name__ == '__main__':
    app.run(debug=True)
