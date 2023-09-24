import requests
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Products.sqlite')
db = SQLAlchemy(app)
# Sample data

class Product(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)


# Endpoint 1: Get all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity} for product in products]
    return jsonify({"products": product_list})

# Endpoint 2: Get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({"product": {"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity}})
    
    else:
        return jsonify({"error": "Task not found"}), 404
    
@app.route('/products/<int:product_id>/remove/<int:quantity>', methods=['POST'])
def remove_product(product_id, quantity):
    product = Product.query.get(product_id)
    if product:
        product.quantity -= quantity 
        if product.quantity < 0:
            return jsonify({"Not enough product in stock"})
        else:
            db.session.commit()
            return jsonify({"removed from inventory": {"quantity": product.quantity}})
    
    else:
        return jsonify({"error": "Task not found"}), 404

#----------------------------------------------------------------------------------------
# Endpoint 3: Create a new product
#add item implies REMOVE additional json object, pass a negative number
@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(name = data['name'], price = data['price'], quantity = data['quantity']) 
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "product created", "product": new_product.id, "name": new_product.name}), 201
#---------------------------------------------------------------------


def get_all_products():
#Retrieve a list of available grocery products, including their names, prices, and quantities in stock
    response = requests.get('http://127.0.0.1:5000/products')
    data = response.json()
    return data

def get_product(product_id):
#Get details about a specific product by its unique ID.
    response = requests.get(f'http://127.0.0.1:5000/products/{product_id}')
    data = response.json()
    return data

def create_product(name):
#Allow the addition of new grocery products to the inventory with information such as name, price, and quantity
    new_product = {"name": name}
    response = requests.post('http://127.0.0.1:5000/products', json=new_product)
    data = response.json()
    return data

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
