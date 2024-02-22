#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    return make_response([bakery.to_dict() for bakery in bakeries], 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        return make_response(bakery.to_dict(), 200)
    return make_response(f'Bakery {id} not found', 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # bakedgoods = BakedGood.query.all()
    # bakedgoods.sort(key=lambda bakedgood: bakedgood.price, reverse=True)
    # return make_response([bakedgood.to_dict() for bakedgood in bakedgoods], 200)
    bakedgoods = BakedGood.query.order_by(BakedGood.price.desc())
    return make_response([bakedgood.to_dict() for bakedgood in bakedgoods])

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    bakedgood = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if bakedgood:
        return make_response(bakedgood.to_dict(), 200)
    return make_response("There aren't any bakedgoods.", 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
