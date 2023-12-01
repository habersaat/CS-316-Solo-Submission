from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.product import Product
from .models.inventory import Inventory
from .models.review import Review
from .models.user import User
from .models.tag import Tag


from flask import Blueprint
bp = Blueprint('product', __name__)

# Product Info Route
@bp.route('/product', methods=['GET', 'POST'])
def product_info():
    # get product id from url
    prod_id = request.args.get('id')

    # get review page from url
    currentPage = request.args.get('review_page') # heads up, I didn't continue with this implementation, but left it here in case anyone wants to implement it

    # get product info by product id
    product = Product.get_all_info_by_id(prod_id)

    # get 10 least expensive products by product id
    seller_products = Inventory.get_10_least_expensive_by_product_id(prod_id)

    # get current page from url
    if currentPage is not None and currentPage != '':
        currentPage = int(currentPage) - 1
    else:
        currentPage = 0

    # get a page of reviews
    reviews = Review.get_paginated_reviews_by_product_id(currentPage, 10, prod_id, None, None)

    # get all tags associated with a product
    tags = Tag.get_tags_by_pid(prod_id)

    # get user for each review and add to the review object
    for review in reviews:
        user = User.get_full_name(review.user_id)
        date = review.timestamp.strftime("%B %d, %Y")
        time = review.timestamp.strftime("%I:%M %p")
        review.user, review.date, review.time = user, date, time

    # render product.html
    return render_template('product.html', title='Product Info', avail_products=product, seller_products=seller_products, tags=tags, reviews=reviews)