from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB

# Create a login manager object
login = LoginManager()
login.login_view = 'users.login'

# Create the application object as an instance of class Flask imported from the flask package
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    app.db = DB(app)
    login.init_app(app)

    # Register the index blueprint
    from .index import bp as index_bp
    app.register_blueprint(index_bp)
    
    # Register the users blueprint
    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    # Register the carts blueprint
    from .carts import bp as cart_bp
    app.register_blueprint(cart_bp)

    # Register the reviews blueprint
    from .reviews import bp as review_bp
    app.register_blueprint(review_bp)

    # Register the purchases blueprint
    from .purchases import bp as purchase_bp
    app.register_blueprint(purchase_bp)

    # Register the inventory blueprint
    from .inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp)

    # Register the products blueprint
    from .product import bp as product_bp
    app.register_blueprint(product_bp)

    # Register the seller blueprint
    from .seller import bp as seller_bp
    app.register_blueprint(seller_bp)

    # Register the newproduct blueprint
    from .newproduct import bp as newproduct_bp
    app.register_blueprint(newproduct_bp)

    # Register the editproduct blueprint
    from .editproduct import bp as editproduct_bp
    app.register_blueprint(editproduct_bp)

    return app
