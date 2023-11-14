from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    cart = db.relationship('Cart', backref='user', uselist=False)



  
    

    cart_products = db.relationship('Product', secondary=cart, backref='users')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)



    def add_to_cart(self, product):
        if product not in self.cart_products:
            self.cart_products.append(product)
            return True
        return False
    
    def remove_from_cart(self, product):
        if product in self.cart_products:
            self.cart_products.remove(product)
            return True
        return False
    
    def clear_cart(self):
        self.cart_products = []


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, default=0.0)
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')

    def update_total_price(self):
        self.total_price = sum(item.subtotal() for item in self.items)
        db.session.commit()

    def remove_all_items(self):
        self.items = []
        self.update_total_price()

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable=False)

    def subtotal(self):
        product = Product.query.get(self.product_id)
        return self.quantity * product.price





class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, title, img_url, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'caption': self.caption,
            'img_url': self.img_url,
            'user_id': self.user_id,
            'author': self.author.username,
            'date_created': self.date_created,
            'last_updated': self.last_updated,
            'like_count': self.like_count(),
        }



