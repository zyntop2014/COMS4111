from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.decorators import login_required
from app import db
import pdb

mod_table = Blueprint('tables', __name__, url_prefix='/tables', template_folder='templates' )

@mod_table.route('/index')
@login_required
def index():
    if request.values.has_key('restaurant_id') and len(request.values['restaurant_id']) > 0:
        restaurant_id= request.values['restaurant_id']
        cur = db.engine.execute("with s(restaurant_id, name, table_id, seats) as (select restaurant.restaurant_id, restaurant.name, restaurant_table.table_id , restaurant_table.seats from restaurant_table, restaurant where restaurant_table.restaurant_id = restaurant.restaurant_id) select * from s where restaurant_id =%s ", restaurant_id)
        rows = cur.fetchall();
        return render_template("tables/index.html", rows=rows)
    else:
        cur = db.engine.execute("select restaurant.restaurant_id, restaurant.name, restaurant_table.table_id , restaurant_table.seats from restaurant_table, restaurant where restaurant_table.restaurant_id = restaurant.restaurant_id")
        rows = cur.fetchall();
        return render_template("tables/index.html", rows=rows)

@mod_table.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        seats= request.form['seats']
        cur = db.engine.execute("select r.restaurant_id, r.name, rt.table_id, rt.seats from restaurant_table rt, restaurant r where rt.restaurant_id = r.restaurant_id and rt.seats >= %s ", [seats])
        rows= cur.fetchall();
        return render_template('tables/search.html', rows1 = rows)
    return render_template('tables/search.html', rows1 = [])

@mod_table.route('/new')
@login_required
def new():
    return render_template('tables/new.html')

@mod_table.route('/edit', methods=['GET'])
@login_required
def edit():
    table_id = request.values['table_id']
    restaurant_id = request.values['restaurant_id']
    cur = db.engine.execute("select * from restaurant_table WHERE table_id=%s AND restaurant_id=%s LIMIT 1", (table_id, restaurant_id))
    table = cur.fetchone()
    return render_template('tables/edit.html', table=table)

@mod_table.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        msg = "Record successfully added"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            table_id= request.form['table_id']
            seats= request.form['seats']
            restaurant_id = request.form['restarant_id']
            connection.execute("INSERT INTO restaurant_table VALUES (%s, %s, %s)", (table_id, seats, restaurant_id))
            trans.commit()
            msg = "Record successfully added"
        except:
            trans.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("result.html", msg=msg, url = url_for('restaurants.main') )
            connnection.close()

@mod_table.route('/update', methods=['POST'])
@login_required
def update():
    if request.method == 'POST':
        msg = "Record successfully added"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            table_id = request.form['update_id']
            seats= request.form['seats']
            restaurant_id = request.form['restaurant_id']
            old_id = request.form['old_id']
            old_restaurant_id = request.form['old_restaurant_id']
            connection.execute("UPDATE restaurant_table SET table_id = %s, seats = %s, restaurant_id = %s WHERE table_id = %s AND restaurant_id = %s", (table_id, seats, restaurant_id, old_id, old_restaurant_id))
            trans.commit()
            msg = "Record successfully updated"
        except:
            trans.rollback()
            msg = "error in update operation"
        finally:
            return render_template("result.html", msg=msg, url = url_for('restaurants.main') )
            connection.close()

@mod_table.route('/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        msg = "Record successfully Deleted"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            id_table= request.form['table_id']
            print id_table
            connection.execute("DELETE  from restaurant_table where table_id= %s ", (id_table,))
            trans.commit()
            msg = "Record successfully Deleted"
        except:
            trans.rollback()
            msg = "error in delete operation"
        finally:
            return render_template("result.html", msg=msg, url = url_for('restaurants.main') )
            connection.close()
