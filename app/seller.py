from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

from .models.inventory import Inventory
from .models.product import Product

from flask import Blueprint
bp = Blueprint('seller', __name__)

# Seller Route
@bp.route('/seller', methods=['GET', 'POST'])
def seller():
    # get seller products
    if current_user.is_authenticated:

        # get seller products by seller id
        seller_products = Inventory.get_inventory_by_sid(current_user.id)

        # start empty list for product names
        product_names = []

        # get product names for each product and add to product_names list
        for product in seller_products:
            product_names.append(Product.get(product.pid).name)

        # add product names to seller_products object
        for i in range(len(seller_products)):
            seller_products[i].name = product_names[i]
            
    # if user is not authenticated, set seller_products to None
    else:
        seller_products = None

    # render seller.html
    return render_template('seller.html', title='Products For Sale', seller_products=seller_products)