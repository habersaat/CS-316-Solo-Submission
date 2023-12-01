from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__) 

# Global variable to keep track of the number of times the index page has been visited. 
# This is used to initialize the database only once. This type of processing would 
# normally take place via a CDN, and thus is very slow to run at first, but doesn't 
# not affect performance after the first run.
visits = 0

# Create index route
@bp.route('/', methods=['GET', 'POST'])
def index():

    # increment the number of visits to the index page
    global visits
    visits += 1

    # Print the number of times the index page has been visited for debugging purposes
    print(f'visits: {visits}')

    # initialize the database if this is the first time the index page has been visited
    if visits == 1:

        # initialize the product rading table. This essentially writes over the randomly 
        # generated ratings and replaces them with the average ratings of the products. 
        # his is efficient on subsequent visits because we update on each review instead 
        # of recalculating the average rating each time.
        Product.product_rating_init() # Can comment out for faster loading

        # initialize the inventory table. This does two thing. First, it sets the product
        # info on the product page to the info of the cheapest instance of that item being
        # sold. Second, it sets low_stock variable correctly according to our definition of
        # low stock.
        Product.inventory_init() # Can comment out for faster loading

        # initialize the shipping speed table. This sets the shipping speed of each product
        # to a time value between 2 and 10 days which is calculated based on the distance
        # between the seller and the buyer. Commented out to avoid the error when the
        # user is not logged in.
        # Product.shipping_speed_init(current_user.longitude, current_user.latitude)

    # get the page number from the url parameters. For reference, the url looks like: /?page=2
    currentPage = request.args.get('page')

    # if currentPage is not None, then convert it to an int
    if currentPage is not None and currentPage != '':
        currentPage = int(currentPage) - 1
    else:
        currentPage = 0

    # get the number of products per page from the url parameters. For reference, the url looks like: /?page=2&n=10
    n = request.args.get('n')

    # if n is not None, then convert it to an int
    if n is not None and n != '':
        n = int(n)
    else:
        n = 12

    # get the filter from the url parameters. For reference, the url looks like: /?page=2&n=10&filter=price_asc
    query = request.args.get('query')
    fil = request.args.get('filter')

    # if fil is not None, then split it into the filter and order
    if fil is not None:
        fil, order = fil.split('_')
    else:
        order = None

    # get the category from the url parameters. For reference, the url looks like: /?page=2&n=10&filter=price_asc&category=electronics
    category = request.args.get('category')

    # get the products from the database based on the url parameters
    products = Product.get_k_page_of_n(currentPage, n, fil, order, category, query)

    # get the stock of each product
    for product in products:
        product.stock = Product.count_product_quantity(product.id)

    # get the number of products in the database based on the url parameters
    length = Product.get_query_length(fil, order, category, query)

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
        
    # render the page by adding information to the index.html file
    return render_template('index.html',
                        avail_products=products,
                        res=length,
                        purchase_history=purchases)

