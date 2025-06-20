from flask import Flask, render_template, request, redirect, url_for
from models import db, Expense
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        category = request.form['category']
        amount = float(request.form['amount'])
        desc = request.form['description']
        db.session.add(Expense(date=date, category=category, amount=amount, description=desc))
        db.session.commit()
        return redirect(url_for('index'))
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/report')
def report():
    data = db.session.query(Expense.category, db.func.sum(Expense.amount)).group_by(Expense.category).all()
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template('report.html', labels=json.dumps(labels), values=json.dumps(values))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
