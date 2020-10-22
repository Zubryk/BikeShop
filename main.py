from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import os 
from cloudipsp import Api, Checkout

UPLOAD_FOLDER = './static'

app = Flask(__name__)
SESSION_TYPE = "redis"
app.config.update(SECRET_KEY=os.urandom(24))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(100))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    wheels = db.Column(db.Integer, nullable=False)
    size = db.Column(db.CHAR, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(100))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=False)

@app.route('/bike_buy/<int:id>')
def bike_buy(id):
    bike = Bike.query.get(id)
    
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "UAH",
        "amount": str(bike.price)+"00"
    }
    url = checkout.url(data).get('checkout_url')
    if bike.amount > 0:
        bike.amount -= 1
        db.session.commit()
        return redirect(url)
    else:
        return "This bike is not available now (:"

@app.route('/item_buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    item.amount -= 1
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "UAH",
        "amount": str(item.price)+"00"
    }
    url = checkout.url(data).get('checkout_url')

    if item.amount > 0:
        return redirect(url)
    else:
        return "This item is not available now (:"

@app.route("/")
def home():
    bikes = Bike.query.all()
    return render_template("home.html", bikes = bikes)

@app.route("/bikes")
def bikes():
    bikes = Bike.query.all()
    return render_template("bikes.html", bikes = bikes)

@app.route("/bikes/<int:id>")
def bike(id):
    bike = Bike.query.get(id)
    return render_template("good.html", bike = bike)

@app.route("/bike_goods")
def bike_goods():
    items = Item.query.all()
    return render_template("goods.html", items = items) 

@app.route("/admin", methods = ['GET', 'POST'])
def admin():
    bikes = Bike.query.all()
    items = Item.query.all()
    return render_template("adminlst.html", bikes = bikes, items = items)

@app.route("/delete_bike/<int:id>", methods = ['GET', 'POST'])
def delete_bike(id):
    bike = Bike.query.get(id)
    db.session.delete(bike)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route("/edit_bike/<int:id>", methods = ['GET', 'POST'])
def edit_bike(id):
    bike = Bike.query.get(id)
    if request.method == 'POST':
        file1 = request.files['inputFile']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        if file1.filename != '':
            file1.save(path)
            bike.photo = file1.filename
        bike.title = request.form["title"]
        bike.description = request.form['description']
        bike.wheels = request.form['wheels']
        bike.size = request.form['size']
        bike.price = request.form["price"]
        bike.amount = request.form["amount"]
        db.session.commit()
        return redirect(url_for('admin'))
    else:
        return render_template('edit_bike.html', bike = bike)

@app.route("/delete_item/<int:id>", methods = ['GET', 'POST'])
def delete_item(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route("/edit_item/<int:id>", methods = ['GET', 'POST'])
def edit_item(id):
    item = Item.query.get(id)
    if request.method == 'POST':
        file1 = request.files['inputFile']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        if file1.filename != '':
            file1.save(path)
            item.photo = file1.filename
        item.title = request.form["title"]
        item.description = request.form['description']
        item.price = request.form["price"]
        item.amount = request.form["amount"]
        db.session.commit()
        return redirect(url_for('admin'))
    else:
        return render_template('edit_item.html', item = item)


@app.route("/admin_add_bike", methods = ['GET', 'POST'])
def admin_add_bike():
    if request.method == 'POST':
        file1 = request.files['inputFile']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        title = request.form["title"]
        description = request.form['description']
        wheels = request.form['wheels']
        size = request.form['size']
        price = request.form["price"]
        amount = request.form["amount"]

        bike = Bike(photo = file1.filename, title=title,description = description, wheels = wheels, size = size, price=price, amount = amount)

        try:
            db.session.add(bike)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template("admin.html")

@app.route("/admin_add_item", methods = ['GET', 'POST'])
def admin_add_item():
    if request.method == 'POST':
        file1 = request.files['inputFile']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        title = request.form["title"]
        description = request.form['description']
        price = request.form["price"]
        amount = request.form["amount"]

        item = Item(photo = file1.filename, title=title, description = description, price=price, amount = amount)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template("add_item.html")

@app.route("/bike_cart/<int:id>", methods = ['GET', 'POST'])
def bike_cart(id):
    bike = Bike.query.get(id)
    if bike.isActive == False:
        bike.isActive = True
    else:
        bike.isActive = False
    db.session.commit()
    return redirect(url_for('bikes'))

@app.route("/item_cart/<int:id>", methods = ['GET', 'POST'])
def item_cart(id):
    item = Item.query.get(id)
    if item.isActive == False:
        item.isActive = True
    else:
        item.isActive = False
    db.session.commit()
    return redirect(url_for('bike_goods'))

@app.route("/cart")
def cart():
    bikes = Bike.query.all()
    items = Item.query.all()
    return render_template("cart.html", bikes = bikes, items = items)

if __name__ == "__main__":
    #db.create_all()
    app.run(debug = True)