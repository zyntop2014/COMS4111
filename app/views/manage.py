from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.decorators import login_required
from app import db
import pdb

mod_manage = Blueprint('manage', __name__, url_prefix='/manage', template_folder='templates' )

@mod_manage.route('/')
@login_required
def index():
    if request.values.has_key('admin_id') and len(request.values['admin_id']) > 0:
        admin_id = request.values['admin_id']
        print admin_id
        cur = db.engine.execute("with s (admin_id, email, restaurant_id, name) as (select m.admin_id, a.email, m.restaurant_id, r.name from manage m, administrator a, restaurant r WHERE m.admin_id = a.admin_id AND m.restaurant_id = r.restaurant_id) select * from s where admin_id = %s", (admin_id,))
        rows = cur.fetchall()
        return render_template('manage/index.html', rows=rows)

    elif request.values.has_key('restaurant_id') and len(request.values['restaurant_id']) > 0:
        restaurant_id = request.values['restaurant_id']
        cur = db.engine.execute("with s (admin_id, email, restaurant_id, name) as (select m.admin_id, a.email, m.restaurant_id, r.name from manage m, administrator a, restaurant r WHERE m.admin_id = a.admin_id AND m.restaurant_id = r.restaurant_id) select * from s where restaurant_id = %s", (restaurant_id,))
        rows = cur.fetchall()
        return render_template('manage/index.html', rows=rows)
    else:
        cur = db.engine.execute("select m.admin_id, a.email, m.restaurant_id, r.name from manage m, administrator a, restaurant r WHERE m.admin_id = a.admin_id AND m.restaurant_id = r.restaurant_id")
        rows = cur.fetchall()
        return render_template('manage/index.html', rows=rows)

@mod_manage.route('/new')
@login_required
def new():
    return render_template('manage/new.html', url = url_for("admins.main"))

@mod_manage.route('/edit', methods=['GET'])
@login_required
def edit():
    restaurant_id = request.values['restaurant_id']
    admin_id = request.values['admin_id']
    cur = db.engine.execute('select * from manage WHERE admin_id= %s AND restaurant_id= %s LIMIT 1', (admin_id, restaurant_id))
    manage = cur.fetchone()
    return render_template('manage/edit.html', manage=manage, url = url_for("admins.main"))

@mod_manage.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            admin_id = request.form['admin_id']
            restaurant_id = request.form['restaurant_id']
            connection.execute("INSERT INTO manage VALUES (%s, %s)", (restaurant_id, admin_id))
            trans.commit()
            msg = "Record successfully added"
        except:
            trans.rollback()
            msg = "error in insert operation"
        finally:
            connection.close()
            return render_template("result.html", msg=msg, url = url_for("admins.main"))

@mod_manage.route('/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            admin_id = request.form['admin_id']
            restaurant_id = request.form['restaurant_id']
            connection.execute("DELETE FROM manage WHERE admin_id= %s AND restaurant_id= %s", (admin_id, restaurant_id))
            trans.commit()
            msg = "Record successfully removed"
        except:
            trans.rollback()
            msg = "error in insert operation"
        finally:
            connection.close()
            return render_template("result.html", msg=msg, url = url_for("admins.main"))

@mod_manage.route('/update', methods=['POST'])
@login_required
def update():
    if request.method == 'POST':
        msg = "Record successfully updated"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            admin_id = request.form['admin_id']
            restaurant_id = request.form['restaurant_id']
            old_restaurant_id = request.form['old_restaurant_id']
            old_admin_id = request.form['old_admin_id']
            db.engine.execute("UPDATE manage SET restaurant_id = %s, admin_id = %s WHERE restaurant_id = %s AND admin_id = %s", (restaurant_id, admin_id, old_restaurant_id, old_admin_id))
            msg = "Record successfully updated"
        except:
            trans.rollback()
            msg = "error in update operation"
        finally:
            connection.close()
            return render_template("result.html", msg=msg, url = url_for('admins.main'))
