from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def check_valid(self):
        if self.price <= 0:
            return False
        if self.amount < 0:
            return False
        return True

class OrderManager:
    def buy(self, product, count):
        if product.amount >= count:
            product.amount = product.amount - count
            return "Готово! Забирайте ваш заказ"
        else:
            return "Упс, булочки закончились"