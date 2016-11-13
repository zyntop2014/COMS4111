from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.decorators import login_required
from app import db
import pdb

mod_party = Blueprint('party', __name__, url_prefix='/party', template_folder='templates' )

def preprocess_string(time):
    return time if len(time) > 0 else None
@mod_party.route('/')
@login_required
def index():
    cur = db.engine.execute("select * from party")
    rows = cur.fetchall();
    return render_template("party/index.html", rows=rows)

@mod_party.route('/new')
@login_required
def new():
    return render_template('party/new.html', url = '/')

@mod_party.route('/edit', methods=['GET'])
@login_required
def edit():
    customer_id = request.values['customer_id']
    party_datetime = request.values['party_datetime']
    cur = db.engine.execute("select * from party WHERE customer_id=%s AND party_datetime=%s LIMIT 1", (customer_id, party_datetime))
    party = cur.fetchone()
    return render_template('party/edit.html', party=party, url='/')

@mod_party.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            size = request.form['size']
            customer_id= request.form['customer_id']
            party_datetime= request.form['party_datetime']
            table_id= preprocess_string(request.form['table_id'])
            restaurant_id= preprocess_string(request.form['restaurant_id'])
            seated_datetime= preprocess_string(request.form['seated_datetime'])
            finish_at= preprocess_string(request.form['finish_at'])
            db.engine.execute("INSERT INTO party VALUES (%s, %s, %s, %s, %s, %s, %s)", (size, customer_id, party_datetime, table_id, restaurant_id, seated_datetime, finish_at))
            trans.commit()
            msg = "Record successfully added"
        except:
            trans.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg, url = "/")
            connection.close()

@mod_party.route('/update', methods=['POST'])
@login_required
def update():
    if request.method == 'POST':
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            size = request.form['size']
            customer_id= request.form['customer_id']
            party_datetime = request.form['party_datetime']
            connection.execute("UPDATE party (size, customer_id, party_datetime) VALUES (%s, %s, %s) WHERE customer_id = %s AND  party_datetime = %s", (size, customer_id, sent_at));
            trans.commit()
            msg = "Record successfully updated"
        except:
            trans.rollback()
            msg = "error in update operation"

        finally:
            return render_template("result.html", msg=msg, url = "/")
            connection.close()

@mod_party.route('/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        msg = "Record successfully Deleted"
        try:
            customer_id= request.form['customer_id']
            party_datetime= request.form['party_time']
            connection.execute("DELETE  from party where customer_id= %s AND party_datetime= %s", (customer_id, party_datetime))
            trans.commit()
            msg = "Record successfully Deleted"
        except:
            trans.rollback()
            msg = "error in delete operation"
        finally:
            return render_template("result.html", msg=msg, url = "/")
            connection.close()

