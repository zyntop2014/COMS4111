from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.decorators import login_required
from app import db
import pdb

mod_customer = Blueprint('customers', __name__, url_prefix='/customers', template_folder='templates' )

@mod_customer.route('/main')
@login_required
def main():
    return render_template('customer/main.html')

@mod_customer.route('/')
@login_required
def index():
    cur = db.engine.execute("SELECT * FROM customer ORDER BY customer_id")
    rows = cur.fetchall();
    return render_template("customer/index.html", rows=rows)

@mod_customer.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('customer/new.html', url="customer")

@mod_customer.route('/edit', methods=['GET'])
@login_required
def edit():
    id = request.values['id']
    cur = db.engine.execute("SELECT * FROM customer WHERE customer_id = %s LIMIT 1", id)
    customer = cur.fetchone()
    return render_template("customer/edit.html", customer=customer)

@mod_customer.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        msg = "Record successfully added"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            idn= request.form['id']
            first_nm = request.form['first_nm']
            last_nm= request.form['last_nm']
            phone = request.form['phone']
            email = request.form['email']
            connection.execute("INSERT INTO customer VALUES (%s, %s, %s, %s, %s)", (idn,first_nm, last_nm, phone, email))
            trans.commit()
            msg = "Record successfully added"
        except:
            trans.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("result.html", msg=msg, url=url_for('customers.main'))
            connection.close()

@mod_customer.route('/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        msg = "Record successfully Deleted"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            id_admin= request.form['id']
            print id_admin
            connection.execute("DELETE from customer where customer_id= %s", id_admin)
            trans.commit()
            msg = "Record successfully Deleted"
        except:
            trans.rollback()
            msg = "error in delete operation"
        finally:
            return render_template("result.html", msg=msg, url = url_for('customers.main'))
            connection.close()

@mod_customer.route('/update', methods=['POST'])
@login_required
def update():
    if request.method == 'POST':
        msg = "Record successfully added"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            customer_id = request.form['update_id']
            first_name= request.form['first_nm']
            last_name = request.form['last_nm']
            phone= request.form['phone']
            email = request.form['email']
            old_id = request.form['old_id']
            connection.execute("UPDATE customer SET customer_id = %s, first_name = %s, last_name = %s, phone_number = %s, customer_email = %s WHERE customer_id = %s", (customer_id, first_name, last_name, phone, email, old_id))
            trans.commit()
            msg = "Record successfully updated"
        except:
            trans.rollback()
            msg = "error in update operation"
        finally:
            return render_template("result.html", msg=msg, url = url_for('customers.main'))
            connection.close()

@mod_customer.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        customer_id= request.form['customer_id']
        cur = db.engine.execute("select * from customer where customer_id= %s", [customer_id])
        rows= cur.fetchall();
        return render_template('customer/search.html', rows1 = rows)
    return render_template('customer/search.html', rows1 = [])

@mod_customer.route('/dinning')
@login_required
def dinning():
    if request.values.has_key('customer_id') and len(request.values['customer_id']) > 0:
        cur = db.engine.execute("with t (customer_id, first_name, last_name, restaurant_id, name, count) as (SELECT c.customer_id, c.first_name, c.last_name, r.restaurant_id, r.name, t.count FROM  (SELECT p.customer_id, p.restaurant_id, COUNT(p.party_datetime) FROM party p, restaurant r WHERE p.restaurant_id = r.restaurant_id GROUP BY p.customer_id, p.restaurant_id ORDER BY customer_id, restaurant_id) t, customer c,restaurant r WHERE t.customer_id = c.customer_id AND r.restaurant_id = t.restaurant_id) select * from t where customer_id = %s", request.values["customer_id"])
        rows = cur.fetchall();
        return render_template('customer/dinning.html', rows= rows)
        #cur = db.engine.execute("SELECT c.customer_id, c.first_name, c.last_name, r.restaurant_id, r.name, t.count FROM t, customer c,restaurant r WHERE t.customer_id = c.customer_id AND r.restaurant_id = t.restaurant_id")
        #rows = cur.fetchall();
        #return render_template('customer/dinning.html', rows= rows)
    else:
        cur = db.engine.execute("SELECT c.customer_id, c.first_name, c.last_name, r.restaurant_id, r.name, t.count FROM (SELECT p.customer_id, p.restaurant_id, COUNT(p.party_datetime) FROM party p, restaurant r WHERE p.restaurant_id = r.restaurant_id GROUP BY p.customer_id, p.restaurant_id ORDER BY customer_id, restaurant_id) t, customer c,restaurant r WHERE t.customer_id = c.customer_id AND r.restaurant_id = t.restaurant_id")
        rows = cur.fetchall();
        return render_template('customer/dinning.html', rows= rows)
