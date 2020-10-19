from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import os 

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
    size = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(100))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)


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
    return render_template("adminlst.html", bikes = bikes)

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
        file1.save(path)
        bike.photo = file1.filename
        bike.title = request.form["title"]
        bike.description = request.form['description']
        bike.wheels = request.form['wheels']
        bike.size = request.form['size']
        bike.price = request.form["price"]
        db.session.commit()
        return redirect(url_for('admin'))
    else:
        return render_template('edit_bike.html', bike = bike)

@app.route("/admin_add", methods = ['GET', 'POST'])
def admin_add():
    if request.method == 'POST':
        file1 = request.files['inputFile']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        title = request.form["title"]
        description = request.form['description']
        wheels = request.form['wheels']
        size = request.form['size']
        price = request.form["price"]

        bike = Bike(photo = file1.filename, title=title,description = description, wheels = wheels, size = size, price=price)

        try:
            db.session.add(bike)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template("admin.html")

if __name__ == "__main__":
    #db.create_all()
    app.run(debug = True)