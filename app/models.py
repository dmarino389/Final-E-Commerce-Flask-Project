# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User model for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Add relationships to other models here, e.g., for orders
    carts = db.relationship('Cart', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(256))  # Add the image URL field

    # Add relationships to other models here, e.g., for orders
    carts = db.relationship('Cart', secondary='cart_product', backref='products_in_cart')

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"

# Define an association table for the many-to-many relationship between Cart and Product
cart_product = db.Table(
    'cart_product',
    db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

# Cart model
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    products = db.relationship('Product', secondary=cart_product, backref='carts_containing_product')

    def __repr__(self):
        return f"Cart(user_id={self.user_id})"
