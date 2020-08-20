from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    price = db.Column(db.Float)
    description = db.Column(db.String(100))

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description


class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "description")


# Init product schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Get a product based on id
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products)


# Create a new product
@app.route('/product', methods=['POST'])
def create_product():
    name = request.json['name']
    price = request.json['price']
    description = request.json['description']

    new_product = Product(name, price, description)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


@app.route('/update/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    product.name = request.json['name']
    product.price = request.json['price']
    product.description = request.json['description']

    db.session.commit()

    return product_schema.jsonify(product)


@app.route('/delete/<id>', methods=['DELETE'])
def delete_product(id):

    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


if __name__ == '__main__':
    app.run(Debug=True)
