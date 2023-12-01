from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from faker import Faker

from .models.user import User
from .models.product import Product


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        # Product.shipping_speed_init(user.longitude, user.latitude) # Initialize shipping speed for all products. Can be commented out for performance
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)



class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

class UpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update')

import psycopg2

@bp.route('/update', methods=['GET', 'POST'])
def update():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = UpdateForm()
    if form.validate_on_submit():
        # update user's information
        current_user.email = form.email.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.address = form.address.data

        # connected to PostgreSQL db
        conn = psycopg2.connect(database="amazon", user="your_username", password="your_password", host="localhost", port="5432")
        # create a Cursor
        c = conn.cursor()

        # execute//?
        c.execute("""
UPDATE Users
SET email = %s, firstname = %s, lastname = %s, address = %s
WHERE id = %s
""", (current_user.email, current_user.firstname, current_user.lastname, current_user.address, current_user.id))

        # commit
        conn.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('users.update'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.address.data = current_user.address
    return render_template('update.html', title='Edit Profile', form=form)
