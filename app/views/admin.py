from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app.decorators import login_required
from app import db
import pdb

mod_admin = Blueprint('admins', __name__, url_prefix='/admins', template_folder='templates' )

@mod_admin.route('/main')
@login_required
def main():
    return render_template('admins/main.html')

@mod_admin.route('/')
@login_required
def index():
    if request.values.has_key('admin_id') and len(request.values['admin_id']) > 0:
        cur = db.engine.execute("select * from administrator where admin_id = %s", request.values["admin_id"])
        rows = cur.fetchall();
        return render_template("admins/index.html", rows=rows)
    else:
        cur = db.engine.execute("select * from administrator ORDER BY admin_id")
        rows = cur.fetchall();
        return render_template("admins/index.html", rows=rows)

@mod_admin.route('/new')
@login_required
def new():
    return render_template('admins/new.html', url = 'admin')

@mod_admin.route('/edit', methods=['GET'])
@login_required
def edit():
    id = request.values['id']
    cur = db.engine.execute("select * from administrator WHERE admin_id = %s LIMIT 1", id)
    admin = cur.fetchone()
    return render_template("admins/edit.html", admin = admin)

@mod_admin.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            idn = request.form['id']
            email = request.form['email']
            nm = request.form['nm']
            pin= request.form['pin']
            connection.execute("INSERT INTO administrator VALUES (%s, %s, %s, %s)", (idn,email, nm, pin))
            trans.commit()
            msg = "Record successfully added"
        except:
            trans.rollback()
            msg = "error in insert operation"
        finally:
            connection.close()
            return render_template("result.html", msg=msg, url = url_for('admins.main') )

@mod_admin.route('/update', methods=['POST'])
@login_required
def update():
    if request.method == 'POST':
        msg = "Record successfully added"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            admin_id = request.form['update_id']
            user_name= request.form['user_name']
            password = request.form['password']
            email= request.form['email']
            old_id = request.form['old_id']
            connection.execute("UPDATE administrator SET admin_id = %s, user_name = %s, email =%s, encrypted_password= %s WHERE admin_id = %s", (admin_id, user_name, email, password, old_id))
            trans.commit()
            msg = "Record successfully updated"
        except:
            trans.rollback()
            msg = "error in update operation"
        finally:
            connection.close()
            return render_template("result.html", msg=msg, url = url_for('admins.main') )

@mod_admin.route('/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        msg = "Record successfully Deleted"
        connection = db.engine.connect()
        trans = connection.begin()
        try:
            id_admin= request.form['id']
            print id_admin
            connection.execute("DELETE  from administrator where admin_id= %s ", (id_admin,))
            trans.commit()
            msg = "Record successfully Deleted"
        except:
            trans.rollback()
            msg = "error in delete operation"
        finally:
            connection.close()
            return render_template("result.html", msg=msg, url = url_for('admins.main') )
