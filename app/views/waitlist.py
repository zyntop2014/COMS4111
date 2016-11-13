from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.decorators import login_required
from app import db

mod_waitlist = Blueprint('waitlists', __name__, url_prefix='/waitlists', template_folder='templates')

@mod_waitlist.route('/')
@login_required
def index():
    if request.values.has_key('restaurant_id') and len(request.values['restaurant_id']) > 0:
        if request.values.has_key('waiting'):
            cur = db.engine.execute("select * from waitlist WHERE restaurant_id=%s AND unlisted_at IS NULL ORDER BY listed_at", request.values['restaurant_id'])
        else:
            cur = db.engine.execute("select * from waitlist WHERE restaurant_id=%s ORDER BY listed_at", request.values['restaurant_id'])
    else:
        if request.values.has_key('waiting'):
            cur = db.engine.execute("select * from waitlist WHERE unlisted_at IS NULL ORDER BY listed_at")
        else:
            cur = db.engine.execute("select * from waitlist ORDER BY listed_at")
    rows = cur.fetchall();
    return render_template("waitlist/index.html", rows=rows)

@mod_waitlist.route('/new')
@login_required
def new():
    return render_template('waitlist/new.html', url='index')

@mod_waitlist.route('/edit', methods=['GET'])
@login_required
def edit():
    restaurant_id = request.values['restaurant_id']
    customer_id = request.values['customer_id']
    party_datetime = request.values['party_datetime']
    cur = db.engine.execute("select * from waitlist WHERE restaurant_id=%s AND customer_id=%s AND party_datetime=%s LIMIT 1", (restaurant_id, customer_id, party_datetime))
    waitlist = cur.fetchone()
    return render_template('waitlist/edit.html', waitlist=waitlist, url='index')

@mod_waitlist.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            restaurant_id = request.form['restaurant_id']
            customer_id= request.form['customer_id']
            party_datetime= request.form['party_datetime']
            listed_at= request.form['listed_at']
            unlisted_at= request.form['unlisted_at']
            unlisted_at = unlisted_at if len(unlisted_at) > 0  else None
            db.engine.execute("INSERT INTO waitlist (restaurant_id, customer_id, party_datetime, listed_at, unlisted_at) VALUES (%s, %s, %s, %s, %s)", (restaurant_id, customer_id, party_datetime, listed_at, unlisted_at))
            trans.commit()
            msg = "Record successfully added"
        except:
            trans.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg, url = "/")
            connection.close()

@mod_waitlist.route('/update', methods=['POST', 'GET'])
@login_required
def update():
    if request.method == 'POST':
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            restaurant_id= request.form['restaurant_id']
            customer_id= request.form['customer_id']
            party_datetime = datetime.strptime(request.form['party_datetime'], "%Y-%m-%d %H:%M:%S")
            listed_at = datetime.strptime(request.form['listed_at'], "%Y-%m-%d %H:%M:%S")
            unlisted_at = datetime.strptime(request.form['unlisted_at'], "%Y-%m-%d %H:%M:%S")
            connection.execute("UPDATE waitlist VALUES (%s, %s) WHERE restaurant_id = %s AND customer_id = %s AND party_datetime = %s", (listed_at, unlisted_at, restaurant_id, customer_id, party_datetime));
            trans.commit()
            msg = "Record successfully updated"
        except:
            trans.rollback()
            msg = "error in update operation"

        finally:
            return render_template("result.html", msg=msg, url = "/")
            connection.close()

@mod_waitlist.route('/delete', methods=['POST', 'GET'])
@login_required
def delete():
    if request.method == 'POST':
        msg = "Record successfully Deleted"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            restaurant_id= request.form['restaurant_id']
            customer_id = request.form['customer_id']
            party_datetime = request.form['party_datetime']
            connection.execute("DELETE  from waitlist where restaurant_id= %s and customer_id = %s and party_datetime = %s ", (restaurant_id, customer_id, party_datetime))
            trans.commit()
            msg = "Record successfully Deleted"
        except:
            trans.rollback()
            msg = "error in delete operation"
        finally:
            return render_template("result.html", msg=msg, url = "/")
            connection.close()
