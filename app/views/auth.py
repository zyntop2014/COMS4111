from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.decorators import login_required
from app import db
import pdb

auth_mod = Blueprint('auth', __name__, template_folder='templates' )

@auth_mod.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    user_password = False
    if request.method == 'POST':
        cur = db.engine
        admins = cur.execute("select * from administrator WHERE user_name=%s AND encrypted_password=%s", (request.form['username'], request.form['password']))
        admin = admins.fetchone();
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            user_password = True 
        if user_password or (admin is not None):
            session['logged_in'] = True
            #flash('You were logged in.')
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@auth_mod.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))
