from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from .forms import RegistrationForm, LoginForm
from .models import User, Product, Cart, CartItem
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from datetime import datetime



@app.route('/')
def home():
  return render_template('index.html')



@app.route("/signup", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('app.feed'))
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(username, email, password)
            
            db.session.add(user)
            db.session.commit()

            flash('Successfully created your account. Sign in now.', "success")
            return redirect(url_for('login'))
        else:
            flash("Invalid form. Please try again.", 'error')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You have been logged out.', 'success')
  return redirect(url_for('list_products'))



## app routes
@app.route('/app', methods=["GET", "POST"])
def app_page():
    return render_template('app.html')


@app.route('/products')
def product_page():
    return render_template('products.html')



@app.route('/products', methods=['GET'])
def all_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/product/<int:product_id>', methods=['GET'])
def single_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return render_template('product.html', product=product)
    return "A product with that ID does not exist.", 404

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    product = Product.query.get(product_id)
    if user.add_to_cart(product):
        db.session.commit()
        return redirect(url_for('show_cart'))
    return "Product already in cart or does not exist."

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    product = Product.query.get(product_id)
    if user.remove_from_cart(product):
        db.session.commit()
        return redirect(url_for('show_cart'))
    return "Product not found in cart or does not exist."

@app.route('/cart', methods=['GET'])
def show_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('cart.html', cart_products=user.cart_products)

@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    user.clear_cart()
    db.session.commit()
    return redirect(url_for('show_cart'))



