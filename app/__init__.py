# Import flask and template operators
from flask import Flask, render_template
from functools import wraps
from decorators import *

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.views.notification import mod_notification
from app.views.auth import auth_mod
from app.views.waitlist import mod_waitlist
from app.views.party import mod_party
from app.views.customer import mod_customer
from app.views.restaurant import mod_restaurant
from app.views.table import mod_table
from app.views.admin import mod_admin

# Register blueprint(s)
app.register_blueprint(mod_notification)
app.register_blueprint(auth_mod)
app.register_blueprint(mod_waitlist)
app.register_blueprint(mod_party)
app.register_blueprint(mod_customer)
app.register_blueprint(mod_restaurant)
app.register_blueprint(mod_table)
app.register_blueprint(mod_admin)
# include other route file here 
#app.register_blueprint(<your file>)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/')
@login_required
def index():
    return render_template('index.html')
