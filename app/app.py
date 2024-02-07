#!/usr/bin/env python3

from flask import Flask, make_response,request,jsonify
from flask_migrate import Migrate

from models import db, Hero,HeroPower,Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>SuperHeroes</h1>'

@app.route('/heroes')
def heroes():
    heroes = []
    for hero in Hero.query.all():
        hero_dict={
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        }
        heroes.append(hero_dict)

    return make_response(heroes, 200)

@app.route('/heroes/<int:id>')
def heroes_by_id(id):
    hero = Hero.query.filter_by(id=id).first()
    if hero:
        response = make_response(hero.to_dict(), 200)
    else:
        response = make_response({'error': 'Hero not found'}, 404)
    return response

@app.route('/powers',methods=['GET'])
def powers():
    powers=[]
    for power in Power.query.all():
        powers.append(power.to_dict())

    if request.method =='GET':
        return make_response(powers,200)
    
@app.route('/powers/<int:id>',methods=['GET','PATCH'])
def powers_by_id(id):
    power = Power.query.filter_by(id=id).first()

    if not power:
        return make_response({'error': 'Power not found'}, 404)

    if request.method == 'GET':
        return make_response(power.to_dict(), 200)
    
    elif request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(power, attr, data[attr])

        db.session.commit()

        return make_response(
            jsonify(power.to_dict()),
            200,
        )
    else:
        return {"errors": ["validation errors"]}
    
@app.route('/hero_powers', methods=['GET', 'POST'])
def hero_powers():
    if request.method == 'GET':
        hero_powers = [hpower.to_dict() for hpower in HeroPower.query.all()]
        return make_response(jsonify(hero_powers), 200)
    
    elif request.method == 'POST':
        data = request.get_json()
        required_fields = ["strength", "power_id", "hero_id"]

        if not all(field in data for field in required_fields):
            return make_response({'errors': ['Validation errors']}, 400)
        

        power = HeroPower(
            strength=data["strength"],
            power_id=data["power_id"],
            hero_id=data["hero_id"]
        )

        db.session.add(power)
        db.session.commit()

        resp = heroes_by_id(power.hero_id)
        
        response = make_response(
            jsonify(resp.to_dict()),
            201,
        )
        return response
    



if __name__ == '__main__':
    app.run(port=5555)
