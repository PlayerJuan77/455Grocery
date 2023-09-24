import os
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Products.sqlite')
#connects code to DB File
db = SQLAlchemy(app)

# Product Model - maps dictionaries(?) into python objects
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    

# Endpoint 1: Get all Products
@app.route('/Products', methods=['GET'])
def get_Products():
    Products = Product.query.all() #gets all the Product objects weve made ^^, and puts them in an array
    Product_list = [{"id": Product.id, "name": Product.name, "price": Product.price, "quantity": Product.quantity} for Product in Products]
    return jsonify({"Products": Product_list})

# Endpoint 2: Get a specific Product by ID
@app.route('/Products/<int:Product_id>', methods=['GET'])
def get_Product(Product_id):
    Product = Product.query.get(Product_id)
    if Product:
        return jsonify({"Product": {"id": Product.id, "name": Product.name, "price": Product.price, "quantity": Product.quantity }})
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint 3: Create a new Product
@app.route('/Products', methods=['POST'])
def create_Product():
    data = request.json
    if "name" not in data:
        return jsonify({"error": "name is required"}), 400

    new_Product = Product(name=data['name'], price=False)
    db.session.add(new_Product)
    db.session.commit()
#commit changes to DB, changes wont take place until you do it to go all at once
    return jsonify({"message": "Product created", "Product": {"id": new_Product.id, "name": new_Product.name, "price": new_Product.price, "quantity": new_Product.quantity}}), 201

#CLIENT PART----------------------------------------------------------------------------------------------------------
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
    app.run(debug=True)    
    #db.create_all() #after the file has been created, comment out so it doesnt continue to create over and over
    all_products = get_all_products()
    print("All products:")
    print(all_products)

    product_id = 2
    specific_product = get_product(product_id)
    print(f"\nproduct {product_id}:")
    print(specific_product)

    new_product_name = "new product"
    created_product = create_product(new_product_name)
    print(f"\nCreated product:")
    print(created_product)
 

