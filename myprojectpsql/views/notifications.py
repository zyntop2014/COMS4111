from flask import Flask, render_template, request, g, redirect, url_for, session, flash
from functools import wraps

@app.route('/notifications')
@login_required
def notification_index():
    con = get_db()
    cur = con.cursor()
    cur.execute("select * from notification")
    rows = cur.fetchall();
    return render_template("notifications/index.html", rows=rows)

@app.route('/notification/create', methods=['POST'])
@login_required
def create_notification():
    if request.method == 'POST':
        try:
            body= request.form['body']
            ntype= request.form['type']
            sent_at= request.form['sent_at']
            restaurant_id= request.form['restaurant_id']
            customer_id= request.form['customer_id']
            with get_db() as con:
                cur = con.cursor()
                cur.execute("INSERT INTO notification VALUES (%s, %s, %s, %s, %s)", (body, ntype, sent_at, restaurant_id, customer_id))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg, url = "/")
            con.close()

@app.route('/notification/edit', methods=['GET'])
@login_required
def edit_notification():
    restaurant_id = request.values['restaurant_id']
    customer_id = request.values['customer_id']
    sent_at = request.values['sent_at']
    con = get_db()
    cur = con.cursor()
    cur.execute("select * from notification WHERE restaurant_id=%s AND customer_id=%s AND sent_at=%s LIMIT 1", (restaurant_id, customer_id, sent_at))
    notification = cur.fetchone()
    return render_template('notifications/edit.html', notification=notification, url='index')

@app.route('/notifications/new')
@login_required
def new_notification():
    return render_template('notifications/new.html', url = 'waitlist')
