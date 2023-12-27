import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI",
                                                       "postgresql://user:password@localhost/db")
db = SQLAlchemy(app)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    status = db.Column(db.String(10), nullable=False)


@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    payment = Payment(amount=data['amount'], currency=data['currency'], status='pending')
    db.session.add(payment)
    db.session.commit()
    return jsonify({"id": payment.id}), 201


@app.route('/payments/<int:id>', methods=['GET'])
def get_payment(id):
    payment = Payment.query.get(id)
    if payment is None:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify({"amount": payment.amount, "currency": payment.currency, "status": payment.status}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
