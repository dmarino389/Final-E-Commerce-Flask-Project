from flask import render_template, url_for, flash, redirect, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import Product, User, Cart
from app.forms import RegistrationForm, LoginForm, ProductForm  # Import your ProductForm


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    # Get the product by ID
    product = Product.query.get_or_404(product_id)
    
    # Check if the user already has a cart, or create a new one if not
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
    
    # Check if the product is already in the user's cart
    if product in cart.products:
        flash(f'{product.name} is already in your cart', 'info')
    else:
        # Add the product to the user's cart
        cart.products.append(product)
        db.session.commit()
        flash(f'Added {product.name} to your cart', 'success')
    
    return redirect(url_for('index'))


@app.route('/cart')
@login_required
def cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if not cart:
        cart_products = []
        total_price = 0
    else:
        cart_products = cart.products
        total_price = sum(product.price for product in cart_products)
    
    return render_template('cart.html', cart_products=cart_products, total_price=total_price)

@app.route('/clear_cart')
@login_required
def clear_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if cart:
        cart.products = []
        db.session.commit()
        flash('Cart cleared', 'success')
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if cart and product in cart.products:
        cart.products.remove(product)
        db.session.commit()
        flash(f'Removed {product.name} from your cart', 'success')
    
    return redirect(url_for('cart'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        flash('Logged in successfully', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    # Logout the user using Flask-Login's built-in function
    logout_user()

    # Clear the session data
    session.clear()

    # Flash a message to indicate successful logout
    flash('You have been logged out successfully!', 'success')

    # Redirect the user to the login page or any other desired page
    return redirect(url_for('login'))




from .forms import ProductForm  # Import your ProductForm

@app.route('/create_product', methods=['GET', 'POST'])
@login_required
def create_product():
    form = ProductForm()  # Create an instance of your ProductForm

    if request.method == 'POST' and form.validate_on_submit():
        # Get form data
        name = form.name.data
        price = form.price.data
        description = form.description.data
        image_url = form.image_url.data

        # Create a new product
        product = Product(name=name, price=price, description=description, image_url=image_url)

        # Add the product to the database
        db.session.add(product)
        db.session.commit()

        flash('Product created successfully', 'success')
        return redirect(url_for('product', product_id=product.id))

    # Render the template with the form
    return render_template('create_product.html', form=form)

