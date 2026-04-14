import os
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bakery.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

@app.route('/')
def home():
    all_products = Product.query.order_by(Product.title).all()
    return render_template('index.html', products=all_products)

@app.route('/login')
def login(): return render_template('login.html')

@app.route('/register')
def register(): return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    products = Product.query.all()

    total_quantity = sum(p.amount for p in products)
    total_value = sum(p.amount * p.price for p in products)

    return render_template('dashboard.html',
                           products=products,
                           total_q=total_quantity,
                           total_v=total_value)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)