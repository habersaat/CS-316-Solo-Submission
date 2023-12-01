from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from werkzeug.datastructures import MultiDict
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField, StringField, TextAreaField, FloatField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

from .models.inventory import Inventory
from .models.product import Product
from .models.tag import Tag

from flask import Blueprint
bp = Blueprint('editproduct', __name__)

# Edit Product Form that allows the user to edit their listed products
class EditProductForm(FlaskForm):

    # Set form fields to be filled out by the user
    userID = IntegerField('ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
    productname = StringField('Product Name', validators=[DataRequired()])
    shortdescription = TextAreaField('Short Description', validators=[DataRequired()])
    longdescription = TextAreaField('Long Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    tags = StringField('Tags')
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    imageurl = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('List Product')

# Edit Product Page
@bp.route('/edit/', methods=['GET', 'POST'])
def editproduct():

    # Set form to be the EditProductForm
    form = EditProductForm()

    # Get the id of the product to be edited
    if current_user.is_authenticated:
        id = request.args.get('id')

        # Get the product instance
        instance = Inventory.get_instance_by_id(id)

        # Get the tags of the product
        tags = Tag.get_tagnames_by_pid(instance.pid)
        tags = ','.join(tags)
        
        # Get the name of the product
        name = Product.get(instance.pid).name

        # Update the product in the inventory
        updatedProduct = Inventory.update_product_in_inventory(instance.id, current_user.id, form.productname.data, form.shortdescription.data, form.longdescription.data, form.category.data, form.tags.data, form.imageurl.data, form.price.data, form.quantity.data)
        
        # If the product was updated, redirect to the seller page
        if updatedProduct:
            return redirect(url_for('seller.seller'))

    # If the user is not authenticated, set the instance to None
    else:
        instance = None

    # Render the edit product page
    return render_template('editproduct.html', title='Edit Product', form=EditProductForm(formdata=MultiDict({
        'productname': name,
        'shortdescription': instance.description_short,
        'longdescription': instance.description_long,
        'category': instance.category,
        'tags': tags,
        'price': instance.price,
        'quantity': instance.quantity,
        'imageurl': instance.image_url
        })), instance=instance, updatedProduct=updatedProduct)

# Delete Product Route (Not an actual page)
@bp.route('/delete/', methods=['GET', 'POST'])
def deleteproduct():

    # Get the id of the product to be deleted
    if current_user.is_authenticated:
        id = request.args.get('id')

        # Get the product instance
        instance = Inventory.get_instance_by_id(id)

        # Delete the product from the inventory
        deletedProduct = Inventory.delete_product_from_inventory(instance.id)

        # If the product was deleted, redirect to the seller page
        if deletedProduct:
            return redirect(url_for('seller.seller'))

    # If the user is not authenticated, set the instance to None
    else:
        instance = None

    # Return None since this is not an actual page
    return None