#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", 
    f"sqlite:///{os.path.join(BASE_DIR, '..', 'instance', 'app.db')}"
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

class Restaurants(Resource):
    def get(self):
        restaurants = [{
            "id": r.id,
            "name": r.name,
            "address": r.address
        } for r in Restaurant.query.all()]
        return restaurants, 200
    
class RestaurantById(Resource):
    def get(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        
        return {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "restaurant_pizzas": [{
                "id": rp.id,
                "price": rp.price,
                "pizza": {
                    "id": rp.pizza.id,
                    "name": rp.pizza.name,
                    "ingredients": rp.pizza.ingredients
                }
            } for rp in restaurant.restaurant_pizzas]
        }, 200

    def delete(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204

class Pizzas(Resource):
    def get(self):
        pizzas = [{
            "id": p.id,
            "name": p.name,
            "ingredients": p.ingredients
        } for p in Pizza.query.all()]
        return pizzas, 200

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        try:
            if not 1 <= data['price'] <= 30:
                raise ValueError("validation errors")  
                
            rp = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id=data['restaurant_id']
            )
            db.session.add(rp)
            db.session.commit()
            
            return {
                "id": rp.id,
                "price": rp.price,
                "pizza_id": rp.pizza_id,
                "restaurant_id": rp.restaurant_id,
                "pizza": {
                    "id": rp.pizza.id,
                    "name": rp.pizza.name,
                    "ingredients": rp.pizza.ingredients
                },
                "restaurant": {
                    "id": rp.restaurant.id,
                    "name": rp.restaurant.name,
                    "address": rp.restaurant.address
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400

api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantById, '/restaurants/<int:id>')
api.add_resource(Pizzas, '/pizzas')
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

if __name__ == "__main__":
    app.run(port=5555, debug=True)