from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('purchases', __name__)


class PurchaseHistoryForm(FlaskForm):
    userID = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('See Purchase History')

@bp.route('/purchases', methods=['GET', 'POST'])
def purchases():
    form = PurchaseHistoryForm()
    recent_purchases = Purchase.get_all_by_uid_since(form.userID.data, datetime.datetime(1980, 9, 14, 0, 0, 0))
    print("Purchase History: ", recent_purchases)
    return render_template('purchases.html', title='Purchase History', form=form, recent_purchases=recent_purchases)