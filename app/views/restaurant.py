from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.decorators import login_required
from app import db
import pdb

mod_restaurant = Blueprint('restaurants', __name__, url_prefix='/restaurants', template_folder='templates' )

@mod_restaurant.route('/main')
@login_required
def main():
    return render_template('restaurants/main.html')

@mod_restaurant.route('/')
@login_required
def index():
    cur = db.engine.execute("SELECT r.restaurant_id, r.name, AVG(w.unlisted_at - w.listed_at) AS avg_waiting FROM restaurant r LEFT JOIN waitlist w ON r.restaurant_id = w.restaurant_id GROUP BY r.restaurant_id ORDER BY avg_waiting")
    rows = cur.fetchall();
    return render_template("restaurants/index.html", rows=rows)

@mod_restaurant.route('/new')
@login_required
def new():
    return render_template('restaurants/new.html')

@mod_restaurant.route('/edit', methods=['GET'])
@login_required
def edit():
    id = request.values['id']
    cur = db.engine.execute("SELECT * FROM restaurant WHERE restaurant_id = %s LIMIT 1", id)
    restaurant = cur.fetchone()
    return render_template("restaurants/edit.html", restaurant=restaurant)

@mod_restaurant.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        msg = "Record successfully added"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            idn = request.form['id']
            nm = request.form['name']
            connection.execute("INSERT INTO restaurant VALUES (%s, %s)", (idn,nm))
            trans.commit()
            msg = "Record successfully added"
        except:
            trans.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("result.html", msg=msg, url = url_for('restaurants.main'))
            connection.close()

@mod_restaurant.route('/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        msg = "Record successfully Deleted"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            restaurant_id= request.form['restaurant_id']
            connection.execute("DELETE  from restaurant where restaurant_id= %s ", (restaurant_id,))
            trans.commit()
            msg = "Record successfully Deleted"
        except:
            trans.rollback()
            msg = "error in delete operation"
        finally:
            return render_template("result.html", msg=msg, url = url_for('restaurants.main'))
            connection.close()

@mod_restaurant.route('/update', methods=['POST'])
@login_required
def update():
    if request.method == 'POST':
        msg = "Record successfully updated"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            restaurant_id = request.form['update_id']
            name= request.form['name']
            old_id = request.form['old_id']
            connection.execute("UPDATE restaurant SET restaurant_id = %s, name = %s WHERE restaurant_id = %s", (restaurant_id, name, old_id))
            trans.commit()
            msg = "Record successfully updated"
        except:
            trans.rollback()
            msg = "error in update operation"
        finally:
            return render_template("result.html", msg=msg, url = url_for('restaurants.main'))
            connection.close()
