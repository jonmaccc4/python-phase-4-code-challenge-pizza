#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

def seed_database():
    with app.app_context():
        print("Deleting old data...")
        RestaurantPizza.query.delete()
        Restaurant.query.delete()
        Pizza.query.delete()

        print("Creating restaurants...")
        r1 = Restaurant(name="Karen's Pizza Shack", address="address1")
        r2 = Restaurant(name="Sanjay's Pizza", address="address2")
        r3 = Restaurant(name="Kiki's Pizza", address="address3")

        print("Creating pizzas...")
        p1 = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
        p2 = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
        p3 = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")

        print("Creating associations...")
        rp1 = RestaurantPizza(restaurant=r1, pizza=p1, price=1)
        rp2 = RestaurantPizza(restaurant=r2, pizza=p2, price=4)
        rp3 = RestaurantPizza(restaurant=r3, pizza=p3, price=5)

        db.session.add_all([r1, r2, r3, p1, p2, p3, rp1, rp2, rp3])
        db.session.commit()
        print("Seeding complete!")

if __name__ == "__main__":
    seed_database()