import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

class item:
    def __init__(self, ID, name, price, quantity):
        self.ID = ID
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_json(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity in cart": self.quantity
        }

cart = []

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_cart(user_id, product_id):
    data = request.json
    quantity = data['quantity']
    r = requests.get(f"https://isaiahs455grocery.onrender.com/products/{product_id}")
    if r.status_code == 404:
        return jsonify({"message": "Product not found"}), 404
    response = r.json()
    product_name = response.get('product', {}).get('name')
    product_price = response.get('product', {}).get('price')
    cart_item = item(product_id, product_name, product_price, quantity)
    cart_id = data.get('row_index', user_id)
    while len(cart) <= cart_id:
        cart.append([])
    cart[cart_id].append(cart_item)
    requests.post(f"https://isaiahs455grocery.onrender.com/products/{product_id}/remove/{quantity}")
    return jsonify({"message": "Added to cart", "cart_item": cart_item.__dict__}), 201

@app.route('/cart/<int:user_id>', methods = ['GET'])
def get_cart(user_id):
    try:
        current_cart = [item.to_json() for item in cart[user_id]]
        return jsonify({"cart": current_cart})
    except IndexError as e:
        return jsonify({"message": "cart empty"})

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['GET'])
def remove_task(user_id, product_id):
    for item in cart[user_id]:
        if item.ID == product_id:
            try:
                cart[user_id].remove(item)
            except IndexError:
                return jsonify({"message": "cart not created"})
        return jsonify("Task deleted")
    else:
        return jsonify({"error": "Task not found"}), 404


# Get the current cart info w name price and quant
def get_cart(user_id):
    response = requests.get('https://isaiahs455grocerycart.onrender.com/cart/{user_id}')
    data = response.json()
    return data

#Will be to remove things out of my cart, specify amount??
def remove_cart(user_id, product_id):
    response = requests.get(f'https://isaiahs455grocerycart.onrender.com/cart/{user_id}/remove/{product_id}')
    data = response.json()
    return data

#to add products to the cart specify number and product id?
def add_cart(user_id, product_id):
    response = requests.post(f'https://isaiahs455grocerycart.onrender.com/cart/{user_id}/add/{product_id}')
    data = response.json()
    return data

if __name__ == '__main__':
    app.run(debug=True, port=5001)
