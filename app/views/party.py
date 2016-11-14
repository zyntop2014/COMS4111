from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.decorators import login_required
from app.utils import get_value
from app import db
import pdb

mod_party = Blueprint('party', __name__, url_prefix='/party', template_folder='templates' )

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
            table_id= get_value(request,'table_id')
            restaurant_id= get_value(request,'restaurant_id')
            seated_datetime= get_value(request,'seated_datetime')
            finish_at= get_value(request, 'finish_at')
            db.engine.execute("INSERT INTO party VALUES (%s, %s, %s, %s, %s, %s, %s)", (size, customer_id, party_datetime, table_id, restaurant_id, seated_datetime, finish_at))
            trans.commit()
            msg = "Record successfully added"
        except:
            trans.rollback()
            msg = "error in insert operation"

        finally:
            connection.close()
            return render_template("result.html", msg=msg, url = "/")

@mod_party.route('/update', methods=['POST'])
@login_required
def update():
    if request.method == 'POST':
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            old_customer_id= request.form['old_customer_id']
            old_party_datetime = request.form['old_party_datetime']
            size = request.form['size']
            customer_id= request.form['customer_id']
            party_datetime = request.form['party_datetime']
            table_id = get_value(request, 'table_id')
            restaurant_id = get_value(request, 'restaurant_id')
            seated_datetime = get_value(request, 'seated_datetime')
            finish_at = get_value(request, 'finish_at')
            connection.execute("UPDATE party SET size=%s, customer_id=%s,party_datetime=%s,table_id=%s,restaurant_id=%s,seated_datetime=%s, finish_at=%s  WHERE customer_id = %s AND  party_datetime = %s", (size, customer_id, party_datetime, table_id, restaurant_id, seated_datetime, finish_at, old_customer_id, old_party_datetime))
            trans.commit()
            msg = "Record successfully updated"
        except:
            trans.rollback()
            msg = "error in update operation"
        finally:
            connection.close()
            return render_template("result.html", msg=msg, url = "/")

@mod_party.route('/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        msg = "Record successfully Deleted"
        connection = db.engine.connect()
        trans = connection.begin()
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
            connection.close()
            return render_template("result.html", msg=msg, url = "/")

