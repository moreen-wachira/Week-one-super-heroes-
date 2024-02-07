from app import app, db
from models import Hero, Power, HeroPower
import random

# Push an application context
app.app_context().push()

# Delete existing data
print("🗑️ Deleting existing data...")
db.session.query(HeroPower).delete()
db.session.query(Hero).delete()
db.session.query(Power).delete()
db.session.commit()

print("🦸‍♀️ Seeding powers...")
powers_data = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
]
powers = []
for data in powers_data:
    power = Power(name=data["name"], description=data["description"])
    powers.append(power)
db.session.add_all(powers)
db.session.commit()

print("🦸‍♀️ Seeding heroes...")
heroes_data = [
    { "name": "Kamala Khan", "super_name": "Ms. Marvel" },
    { "name": "Doreen Green", "super_name": "Squirrel Girl" },
    { "name": "Gwen Stacy", "super_name": "Spider-Gwen" },
    { "name": "Janet Van Dyne", "super_name": "The Wasp" },
    { "name": "Wanda Maximoff", "super_name": "Scarlet Witch" },
    { "name": "Carol Danvers", "super_name": "Captain Marvel" },
    { "name": "Jean Grey", "super_name": "Dark Phoenix" },
    { "name": "Ororo Munroe", "super_name": "Storm" },
    { "name": "Kitty Pryde", "super_name": "Shadowcat" },
    { "name": "Elektra Natchios", "super_name": "Elektra" }
]

heroes = []
for data in heroes_data:
    hero = Hero(**data)
    heroes.append(hero)

db.session.add_all(heroes)
db.session.commit()

print("🦸‍♀️ Adding powers to heroes...")
strengths = ["Strong", "Weak", "Average"]
for hero in heroes:
    for _ in range(random.randint(1, 3)):
        power = random.choice(powers)
        hero_power = HeroPower(hero=hero, power=power, strength=random.choice(strengths))
        db.session.add(hero_power)

db.session.commit()
print("🦸‍♀️ Done seeding!")
