from flask import Flask, jsonify, request
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.Config')

if __name__ == "__main__":
    app.run()


db = SQLAlchemy(app)
ma = Marshmallow(app)


migrate = Migrate()
migrate.init_app(app, db)

now = datetime.now().strftime('%d-%m-%y %H:%M:%S')

'''MODELS'''


class Category(db.Model):
    __tablename__ = 'category'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), unique=True, nullable=False)
    products: str = db.relationship("Product", backref='category', lazy='dynamic')
    details: str = db.Column(db.String(200))
    created = db.Column(db.DateTime())

    # updated = db.Column(db.DateTime())

    def __init__(self, name: str, details: str) -> None:
        self.name = name
        self.details = details
        self.created = now

    def __str__(self) -> str:
        return f'{self.name}'


class Product(db.Model):
    __tablename__ = 'product'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), unique=True, nullable=False)
    category_id: int = db.Column(db.Integer, db.ForeignKey('category.id'))
    quantity: float = db.Column(db.Float)
    price: float = db.Column(db.Float)
    details: str = db.Column(db.String(200))
    created = db.Column(db.DateTime())

    # updated = db.Column(db.DateTime())

    def __init__(self, name: str, category_id: int, quantity: float, price: float, details: str, ) -> None:
        self.name = name
        self.category_id = category_id
        self.quantity = quantity
        self.price = price
        self.details = details
        self.created = now

    def __str__(self) -> str:
        return f'{self.name} price: {self.price}, quantity: {self.quantity}'


db.create_all()

'''SERIALIZERS'''


class ProductSchema(ma.Schema):
    class Meta:
        fields: tuple = ('id', 'name', 'category_id', 'quantity', 'price', 'details', 'created',)


class ProductsSchema(ma.Schema):
    class Meta:
        fields: tuple = ('id', 'name', 'category_id', 'quantity', 'price', 'details',)


class CategorySchema(ma.Schema):
    class Meta:
        fields: tuple = ('id', 'name', 'details', 'created',)


class CategoriesSchema(ma.Schema):
    class Meta:
        fields: tuple = ('id', 'name', 'details',)


product_schema = ProductSchema()
products_schema = ProductsSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategoriesSchema(many=True)


@app.route('/', methods=['GET'])
@app.route("/home", methods=['GET'])
@app.route("/index", methods=['GET'])
def index() -> dict:
    return jsonify({'message': 'Welcome to my API.'})


@app.route('/products', methods=['GET', 'POST'])
def create_product() -> dict:
    if request.method == 'GET':
        all_products: list = Product.query.all()
        result: list = products_schema.dump(all_products)
        return jsonify(result)

    if request.method == 'POST':
        name: str = request.json['name']
        category_id: int = request.json['category_id']
        quantity: float = request.json['quantity']
        price: float = request.json['price']
        details: float = request.json['details']

        new_product: Product = Product(name, category_id, quantity, price, details)

        db.session.add(new_product)
        db.session.commit()

        return product_schema.jsonify(new_product)


@app.route('/products/<int:_id>', methods=['GET'])
def get_product(_id: int) -> dict:
    product: list = Product.query.get(_id)
    return product_schema.jsonify(product)


@app.route('/products/<int:_id>', methods=['PUT'])
def update_product(_id: int) -> dict:
    product: list = Product.query.get(_id)

    name: str = request.json['name']
    category_id: int = request.json['category_id']
    quantity: float = request.json['quantity']
    price: float = request.json['price']
    details: float = request.json['details']

    product.name = name
    product.category_id = category_id
    product.quantity = quantity
    product.price = price
    product.details = details
    # product.updated = now.strftime("%H:%M:%S")

    db.session.commit()

    return product_schema.jsonify(product)


@app.route('/products/<id>', methods=['DELETE'])
def delete_product(_id) -> dict:
    product: list = Product.query.get(_id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)


'''CATEGORIES ENDPOINTS'''


@app.route('/categories', methods=['GET'])
def get_categories() -> dict:
    all_categories: list = Category.query.all()
    result = categories_schema.dump(all_categories)
    return jsonify(result)


# Create a new category if post, or list all
@app.route('/categories', methods=['POST', 'GET'])
def create_category() -> dict:
    print(request.json)
    name: str = request.json['name']
    details: str = request.json['details']
    #    created: = now.strftime("%H:%M:%S")

    new_category: Category = Category(name, details, )

    db.session.add(new_category)
    db.session.commit()

    return category_schema.jsonify(new_category)