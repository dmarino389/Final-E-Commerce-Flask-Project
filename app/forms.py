from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# User registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# User login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=3, max=128)])
    price = StringField('Price', validators=[DataRequired()])
    description = TextAreaField('Product Description', validators=[DataRequired()])
    image_url = StringField('Image URL')  # Add the image URL field
    submit = SubmitField('Create Product')



class AddToCartForm(FlaskForm):
    product_id = SelectField('Select Product', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add to Cart')

    def __init__(self, *args, **kwargs):
        super(AddToCartForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(product.id, product.name) for product in Product.query.all()]
