from flask import Flask, render_template, request, g, redirect, url_for, session, flash
from functools import wraps
import psycopg2
from datetime import datetime
import pdb

app = Flask(__name__)
app.secret_key = 'my precious'

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            #flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    user_password = False

    if request.method == 'POST':

        db = get_db()
        cur=db.cursor()
        cur.execute("select * from administrator WHERE user_name=%s AND encrypted_password=%s", (request.form['username'], request.form['password']))
        admin = cur.fetchone();

        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            user_password = True 

        if user_password or (admin is not None):
            session['logged_in'] = True
            #flash('You were logged in.')
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))

def get_db():
#   db = psycopg2.connect("dbname='database' user='postgres' host='localhost' password='580430'")
#    db = psycopg2.connect("dbname='postgres' user='yz3054' host='104.196.175.120' password='h7fmz'")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/waitlist')
@login_required
def waitlist():
    return render_template('waitlist.html')


@app.route('/restaurant')
@login_required
def restaurant():
    return render_template('restaurant.html')


@app.route('/dinning')
@login_required
def dinning():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT c.customer_id, c.first_name, c.last_name, r.restaurant_id, r.name, t.count FROM (SELECT p.customer_id, p.restaurant_id, COUNT(p.party_datetime) FROM party p, restaurant r WHERE p.restaurant_id = r.restaurant_id GROUP BY p.customer_id, p.restaurant_id ORDER BY customer_id, restaurant_id) t, customer c,restaurant r WHERE t.customer_id = c.customer_id AND r.restaurant_id = t.restaurant_id")
    rows = cur.fetchall();
    return render_template('dinning.html', rows= rows)

@app.route('/customer')
@login_required
def customer():
    return render_template('customer.html')


@app.route('/customerlist')
@login_required
def list():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM customer ORDER BY customer_id")
    rows = cur.fetchall();
    return render_template("customerlist.html", rows=rows)



@app.route('/restaurantlist')
@login_required
def retaurantlist():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT r.restaurant_id, r.name, AVG(w.unlisted_at - w.listed_at) AS avg_waiting FROM waitlist w, restaurant r WHERE w.restaurant_id = r.restaurant_id GROUP BY r.restaurant_id ORDER BY avg_waiting")
    rows = cur.fetchall();
    return render_template("restaurantlist.html", rows=rows)

@app.route('/restaurantlist2')
@login_required
def retaurantlist2():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT restaurant_id, name FROM restaurant ORDER BY restaurant_id")
    rows = cur.fetchall();
    return render_template("restaurantlist2.html", rows=rows)

@app.route('/tablelist')
@login_required
def tablelist():
    con = get_db()
    cur = con.cursor()
    cur.execute("select restaurant.restaurant_id, restaurant.name, restaurant_table.table_id , restaurant_table.seats from restaurant_table, restaurant where restaurant_table.restaurant_id = restaurant.restaurant_id")
    rows = cur.fetchall();
    return render_template("tablelist.html", rows=rows)


@app.route('/adminlist')
@login_required
def adminlist():
    con = get_db()
    cur = con.cursor()
    cur.execute("select * from administrator ORDER BY admin_id")
    rows = cur.fetchall();
    return render_template("adminlist.html", rows=rows)



@app.route('/enteradmin')
@login_required
def new_admin():
    return render_template('enteradmin.html', url = 'admin')

@app.route('/waitlistcustomer')
@login_required
def add_customer_waitlist():
    con = get_db()
    cur = con.cursor()
    cur.execute("select * from restaurant")
    restaurants = cur.fetchall()
    con.commit()
    cur.execute("select * from customer")
    customers = cur.fetchall()
    con.commit()
    return render_template('waitlistcustomer.html', restaurants=restaurants, customers=customers, url = 'index')




@app.route('/entercustomer', methods=['GET', 'POST'])
@login_required
def entercustomer():
    return render_template('entercustomer.html', url="customer")




@app.route('/entermanage')
@login_required
def new_manage():
    return render_template('entermanage.html', url = 'admin')

@app.route('/entertable')
@login_required
def new_table():
    return render_template('entertable.html')





@app.route('/enterrestaurant')
@login_required
def new_restaurant():
    return render_template('enterrestaurant.html')

@app.route('/addrecadmin', methods=['POST', 'GET'])
@login_required
def addrecadmin():
    if request.method == 'POST':

        
        try:
            
            idn = request.form['id']
            email = request.form['email']
            nm = request.form['nm']
            pin= request.form['pin']
            

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("INSERT INTO administrator VALUES (%s, %s, %s, %s)", (idn,email, nm, pin))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("enteradmin.html", msg=msg, url = "admin")
            con.close()

@app.route('/add_customer_to_waitlist', methods=['POST'])
@login_required
def add_customer_to_waitlist():
    if request.method == 'POST':
        try:
            restaurant_id = request.form['restaurant_id']
            customer_id= request.form['customer_id']
            party_size = request.form['party_size']
            party_datetime= datetime.datetime.now()
            listed_at= datetime.datetime.now()

            with get_db() as con:
                cur = con.cursor()
                cur.execute("INSERT INTO party (size, customer_id, party_datetime) VALUES (%s, %s, %s)", (party_size, customer_id, party_datetime))
                cur.execute("INSERT INTO waitlist (restaurant_id, customer_id, party_datetime, listed_at) VALUES (%s, %s, %s, %s)", (restaurant_id, customer_id, party_datetime, listed_at))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("waitlistlist.html", url = "/")
            con.close()






@app.route('/addrecmanage', methods=['POST', 'GET'])
@login_required
def addrecmanage():
    if request.method == 'POST':

        
        try:
            
            idn = request.form['admin_id']
            res_id = request.form['res_id']

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("INSERT INTO manage VALUES (1, 1)")
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("entermanage.html", msg=msg, url = "admin")
            con.close()


@app.route('/addreccustomer', methods=['POST', 'GET'])
@login_required
def addreccustomer():
    if request.method == 'POST':

        msg = "Record successfully added"
        try:
            idn= request.form['id']
            first_nm = request.form['first_nm']
            last_nm= request.form['last_nm']
            phone = request.form['phone']
            email = request.form['email']

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("INSERT INTO customer VALUES (%s, %s, %s, %s, %s)", (idn,first_nm, last_nm, phone, email))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("entercustomer.html", msg=msg, url = "customer")
            con.close()

@app.route('/addrectable', methods=['POST', 'GET'])
@login_required
def addrectable():
    if request.method == 'POST':

        msg = "Record successfully added"
        try:
            table_id= request.form['table_id']
            seats= request.form['seats']
            restaurant_id = request.form['restarant_id']
            
           

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("INSERT INTO restaurant_table VALUES (%s, %s, %s)", (table_id, seats, restaurant_id))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("entertable.html", msg=msg, url = "restaurant")
            con.close()


@app.route('/addrecrestaurant', methods=['POST', 'GET'])
@login_required
def addrecrestaurant():
    if request.method == 'POST':

        msg = "Record successfully added"
        try:
            
            idn = request.form['id']
            nm = request.form['nm']
            

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("INSERT INTO restaurant VALUES (%s, %s)", (idn,nm))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("enterrestaurant.html", msg=msg, url = "restaurant")
            con.close()


@app.route('/searchtable', methods=['GET', 'POST'])
@login_required
def searchtable():
    if request.method == "POST":
        db = get_db()
        cur=db.cursor()
        restaurant_name= request.form['restaurant_name']
        seats= request.form['seats']
        cur.execute("select r.restaurant_id, r.name, rt.table_id, rt.seats from restaurant_table rt, restaurant r where rt.restaurant_id = r.restaurant_id and rt.seats >= %s ", [seats])
        rows= cur.fetchall();
        return render_template('searchtable.html', rows1 = rows)
    return render_template('searchtable.html', rows1 = [])

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        db = get_db()
        cur=db.cursor()
        customer_id= request.form['customer_id']
        cur.execute("select * from customer where customer_id= %s", [customer_id])
        rows= cur.fetchall();
        return render_template('search.html', rows1 = rows)
    return render_template('search.html', rows1 = [])
        
@app.route('/search2', methods=['GET', 'POST'])
@login_required
def search2():
    if request.method == "POST":
        db = get_db()
        cur=db.cursor()
        customer_id= request.form['customer_id']
        cur.execute("select * from customer where customer_id= %s", [customer_id])
        rows= cur.fetchall();
        return render_template('search.html', rows2 = rows)
    return render_template('search.html', rows2 = [])   


@app.route('/deleteadmin', methods=['POST', 'GET'])
@login_required
def deleteadmin():
    if request.method == 'POST':

        msg = "Record successfully Deleted"
        try:
            id_admin= request.form['id']
            print id_admin
        
            with get_db() as con:
                cur = con.cursor()    
                cur.execute("DELETE  from administrator where admin_id= %s ", (id_admin,))
                con.commit()
                msg = "Record successfully Deleted"
        except:
            con.rollback()
            msg = "error in delete operation"

        finally:
            return render_template("result.html", msg=msg, url = "admin")
            con.close()

@app.route('/unlistcustomer', methods=['POST', 'GET'])
@login_required
def unlistcustomer():
    if request.method == 'POST':

        msg = "Customer successfully Unlisted"
        try:
            restaurant_id= request.form['restaurant_id']
            customer_id = request.form['customer_id']
            party_datetime = request.form['party_datetime']
            with get_db() as con:
                cur = con.cursor()    
                cur.execute("UPDATE waitlist SET unlisted_at = now() WHERE restaurant_id= %s and customer_id = %s and party_datetime = %s ", (restaurant_id, customer_id, party_datetime))
                con.commit()
                msg = "Record successfully Unlisted"
        except:
            con.rollback()
            msg = "error in update operation"

        finally:
            return render_template("result.html", msg=msg, url = "/")
            con.close()





    
@app.route('/deletetable', methods=['POST', 'GET'])
@login_required
def deletetable():
    if request.method == 'POST':

        #msg = "Record successfully Deleted"
        try:
            id_table= request.form['table_id']
            print id_table
         
        

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("DELETE  from restaurant_table where table_id= %s ", (id_table,))
                con.commit()
                msg = "Record successfully Deleted"
        except:
            con.rollback()
            msg = "error in delete operation"

        finally:
            return render_template("result.html", msg=msg, url = "restaurant")
            con.close()


@app.route('/deleterestaurant', methods=['POST', 'GET'])
@login_required
def deleterestaurant():
    if request.method == 'POST':

        #msg = "Record successfully Deleted"
        try:
            restaurant_id= request.form['restaurant_id']
          
         
        

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("DELETE  from restaurant where restaurant_id= %s ", (restaurant_id,))
                con.commit()
                msg = "Record successfully Deleted"
        except:
            con.rollback()
            msg = "error in delete operation"

        finally:
            return render_template("result.html", msg=msg, url = "restaurant")
            con.close()

@app.route('/deletecustomer', methods=['POST', 'GET'])
@login_required
def deletecustomer():
    if request.method == 'POST':

        msg = "Record successfully Deleted"
        try:
            id_admin= request.form['id']
            print id_admin
            
        

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("DELETE  from customer where customer_id= %s", (id_admin,))
                con.commit()
                msg = "Record successfully Deleted"
        except:
            con.rollback()
            msg = "error in delete operation"

        finally:
            return render_template("result.html", msg=msg, url = "customer")
            con.close()

@app.route('/updatecustomer', methods=['POST', 'GET'])
@login_required
def updatecustomer():
    old_id = request.form['old_id']
    return render_template("updatecustomer.html", old_id = old_id)

@app.route('/addrecupdatecustomer', methods=['POST', 'GET'])
@login_required
def addrecupdatecustomer():
    if request.method == 'POST':

        msg = "Record successfully added"
        try:
            customer_id = request.form['update_id']
            first_name= request.form['first_nm']
            last_name = request.form['last_nm']
            phone= request.form['phone']
            email = request.form['email']
            old_id = request.form['old_id']
           

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("UPDATE customer SET customer_id = %s, first_name = %s, last_name = %s, phone_number = %s, customer_email = %s WHERE customer_id = %s", (customer_id, first_name, last_name, phone, email, old_id))
                con.commit()
                msg = "Record successfully updated"
        except:
            con.rollback()
            msg = "error in update operation"

        finally:
            return render_template("customer.html")
            con.close()

@app.route('/updatetable', methods=['POST', 'GET'])
@login_required
def updatetable():
    old_id = request.form['old_id']
    return render_template("updatetable.html", old_id = old_id)

@app.route('/addrecupdatetable', methods=['POST', 'GET'])
@login_required
def addrecupdatetable():
    if request.method == 'POST':

        msg = "Record successfully added"
        try:
            table_id = request.form['update_id']
            seats= request.form['seats']
            restaurant_id = request.form['restaurant_id']
            old_id = request.form['old_id']
           

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("UPDATE restaurant_table SET table_id = %s, seats = %s, restaurant_id = %s WHERE table_id = %s", (table_id, seats, restaurant_id, old_id))
                con.commit()
                msg = "Record successfully updated"
        except:
            con.rollback()
            msg = "error in update operation"

        finally:
            return render_template("restaurant.html")
            con.close()
   

@app.route('/updateadmin', methods=['POST', 'GET'])
@login_required
def updateadmin():
    old_id = request.form['old_id']
    return render_template("updateadmin.html", old_id = old_id)

@app.route('/addrecupdateadmin', methods=['POST', 'GET'])
@login_required
def addrecupdateadmin():
    if request.method == 'POST':

        msg = "Record successfully added"
        try:
            admin_id = request.form['update_id']
            user_name= request.form['user_name']
            password = request.form['password']
            email= request.form['email']
            old_id = request.form['old_id']
           

            with get_db() as con:
                cur = con.cursor()    
                cur.execute("UPDATE administrator SET admin_id = %s, user_name = %s, email =%s, encrypted_password= %s WHERE admin_id = %s", (admin_id, user_name, email, password, old_id))
                con.commit()
                msg = "Record successfully updated"
        except:
            con.rollback() 
            msg = "error in update operation"

        finally:
            return render_template("admin.html")
            con.close()

@app.route('/updaterestaurant', methods=['POST', 'GET'])
@login_required
def updaterestaurant():
    old_id = request.form['old_id']
    return render_template("updaterestaurant.html", old_id = old_id)

@app.route('/addrecupdaterestaurant', methods=['POST', 'GET'])
@login_required
def addrecupdaterestaurant():
    if request.method == 'POST':
        msg = "Record successfully added"
        try:
            restaurant_id = request.form['update_id']
            name= request.form['name']
            old_id = request.form['old_id']
            with get_db() as con:
                cur = con.cursor()    
                cur.execute("UPDATE restaurant SET restaurant_id = %s, name = %s WHERE restaurant_id = %s", (restaurant_id, name, old_id))
                con.commit()
                msg = "Record successfully updated"
        except:
            con.rollback() 
            msg = "error in update operation"

        finally:
            return render_template("restaurant.html")
            con.close()