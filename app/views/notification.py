from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.decorators import login_required
from app import db

mod_notification = Blueprint('notifications', __name__, url_prefix='/notifications', template_folder='templates' )

@mod_notification.route('/')
@login_required
def index():
    cur = db.engine.execute("select * from notification")
    rows = cur.fetchall();
    return render_template("notifications/index.html", rows=rows)

@mod_notification.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            body= request.form['body']
            ntype= request.form['type']
            sent_at= request.form['sent_at']
            restaurant_id= request.form['restaurant_id']
            customer_id= request.form['customer_id']
            connection.execute("INSERT INTO notification VALUES (%s, %s, %s, %s, %s)", (body, ntype, sent_at, restaurant_id, customer_id))
            trans.commit()
            msg = "Record successfully added"
        except:
            trans.rollback()
            msg = "error in insert operation"
        finally:
            connection.close()
            return render_template("result.html", msg=msg, url = "/")

@mod_notification.route('/edit', methods=['GET'])
@login_required
def edit():
    restaurant_id = request.values['restaurant_id']
    customer_id = request.values['customer_id']
    sent_at = request.values['sent_at']
    cur = db.engine.execute("select * from notification WHERE restaurant_id=%s AND customer_id=%s AND sent_at=%s LIMIT 1", (restaurant_id, customer_id, sent_at))
    notification = cur.fetchone()
    return render_template('notifications/edit.html', notification=notification, url='/')

@mod_notification.route('/new')
@login_required
def new():
    return render_template('notifications/new.html', url = '/')

@mod_notification.route('/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        connection = db.engine.connect()
        trans = connection.begin()
        msg = "Record successfully Deleted"
        try:
            sent_at= request.form['sent_at']
            restaurant_id= request.form['restaurant_id']
            customer_id= request.form['customer_id']
            connection.execute("DELETE  from notification where sent_at=%s AND restaurant_id =%s and customer_id= %s", (sent_at, restaurant_id, customer_id))
            trans.commit()
            msg = "Record successfully Deleted"
        except:
            trans.rollback()
            msg = "error in delete operation"
        finally:
            connection.close()
            return render_template("result.html", msg=msg, url = "/")

@mod_notification.route('/update', methods=['POST'])
@login_required
def update():
    if request.method == 'POST':
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            old_restaurant_id= request.form['old_restaurant_id']
            old_customer_id= request.form['old_customer_id']
            old_sent_at = request.form['old_sent_at']
            restaurant_id= request.form['restaurant_id']
            customer_id= request.form['customer_id']
            sent_at = request.form['sent_at']
            notif_type = request.form['type']
            body = request.form['body']
            connection.execute("UPDATE notification SET restaurant_id = %s, customer_id = %s, sent_at = %s, type = %s, body = %s WHERE restaurant_id = %s AND customer_id = %s AND sent_at = %s", (restaurant_id, customer_id, sent_at, notif_type, body, old_restaurant_id, old_customer_id, old_sent_at))
            trans.commit()
            msg = "Record successfully updated"
        except:
            trans.rollback()
            msg = "error in update operation"
        finally:
            connection.close()
            return render_template("result.html", msg=msg, url = "/")
