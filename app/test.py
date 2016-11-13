from flask import Flask, render_template, request, g, redirect, url_for, session, flash
from functools import wraps
import psycopg2
from datetime import datetime
import pdb

app = Flask(__name__)
app.secret_key = 'my precious'

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            #flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    user_password = False

    if request.method == 'POST':

        db = get_db()
        cur=db.cursor()
        cur.execute("select * from administrator WHERE user_name=%s AND encrypted_password=%s", (request.form['username'], request.form['password']))
        admin = cur.fetchone();

        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            user_password = True 

        if user_password or (admin is not None):
            session['logged_in'] = True
            #flash('You were logged in.')
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))

def get_db():
#   db = psycopg2.connect("dbname='database' user='postgres' host='localhost' password='580430'")
#    db = psycopg2.connect("dbname='postgres' user='yz3054' host='104.196.175.120' password='h7fmz'")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/waitlist')
@login_required
def waitlist():
    return render_template('waitlist.html')


@app.route('/waitlistcustomer')
@login_required
def add_customer_waitlist():
    con = get_db()
    cur = con.cursor()
    cur.execute("select * from restaurant")
    restaurants = cur.fetchall()
    con.commit()
    cur.execute("select * from customer")
    customers = cur.fetchall()
    con.commit()
    return render_template('waitlistcustomer.html', restaurants=restaurants, customers=customers, url = 'index')

@app.route('/entermanage')
@login_required
def new_manage():
    return render_template('entermanage.html', url = 'admin')


@app.route('/add_customer_to_waitlist', methods=['POST'])
@login_required
def add_customer_to_waitlist():
    if request.method == 'POST':
        try:
            restaurant_id = request.form['restaurant_id']
            customer_id= request.form['customer_id']
            party_size = request.form['party_size']
            party_datetime= datetime.datetime.now()
            listed_at= datetime.datetime.now()

            with get_db() as con:
                cur = con.cursor()
                cur.execute("INSERT INTO party (size, customer_id, party_datetime) VALUES (%s, %s, %s)", (party_size, customer_id, party_datetime))
                cur.execute("INSERT INTO waitlist (restaurant_id, customer_id, party_datetime, listed_at) VALUES (%s, %s, %s, %s)", (restaurant_id, customer_id, party_datetime, listed_at))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("waitlistlist.html", url = "/")
            con.close()

@app.route('/addrecmanage', methods=['POST', 'GET'])
@login_required
def addrecmanage():
    if request.method == 'POST':

        
        try:
            
            idn = request.form['admin_id']
            res_id = request.form['res_id']

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("INSERT INTO manage VALUES (1, 1)")
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("entermanage.html", msg=msg, url = "admin")
            con.close()




@app.route('/unlistcustomer', methods=['POST', 'GET'])
@login_required
def unlistcustomer():
    if request.method == 'POST':

        msg = "Customer successfully Unlisted"
        try:
            restaurant_id= request.form['restaurant_id']
            customer_id = request.form['customer_id']
            party_datetime = request.form['party_datetime']
            with get_db() as con:
                cur = con.cursor()    
                cur.execute("UPDATE waitlist SET unlisted_at = now() WHERE restaurant_id= %s and customer_id = %s and party_datetime = %s ", (restaurant_id, customer_id, party_datetime))
                con.commit()
                msg = "Record successfully Unlisted"
        except:
            con.rollback()
            msg = "error in update operation"

        finally:
            return render_template("result.html", msg=msg, url = "/")
            con.close()
