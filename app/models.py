# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model,SerializerMixin):
    __tablename__ = 'hero'
    serialize_rules=('-heropowers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heropowers = db.relationship('HeroPower', backref='hero')

    def __repr__(self):
        return f'{self.name} has {self.super_name}'

class HeroPower(db.Model,SerializerMixin):
    __tablename__ = 'heropowers'

    serialize_rules=('-hero.heropowers',)
    serialize_rules=('-power.heropowers',)

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String) 

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    @validates('strength')
    def validate_strength(self,key,strength):
        strengths=['Strong', 'Weak', 'Average']
        if strength not in strengths:
            raise ValueError('The strength should be either Strong, Weak, Average')
        return strength

class Power(db.Model,SerializerMixin):
    __tablename__='powers'
    serialize_rules=('-heropowers.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heropowers = db.relationship('HeroPower', backref='power')

    @validates('description')
    def validate_description(self,key,description):
        if not description:
            raise ValueError("The power must be described")
        if len(description) < 20:
            raise ValueError("The description should exceed 20 characters")
        return description

    def __repr__(self):
        return f'{self.name} has {self.powers} powers'