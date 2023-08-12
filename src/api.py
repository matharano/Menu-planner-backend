from flask_restx import Api, Resource, fields
from http import HTTPStatus

from .database import Database

api = Api(title='Natural Club Menu Planner', description='API for managing the menu planner web app, and talk to the SQL database')
dishes_ns = api.namespace('dishes', description='Dish management')
db = Database()

message_model = api.model("message", {
   "message": fields.String
})

dish_model = api.model('dish', {
    'id' : fields.Integer,
    'category': fields.String,
    'name': fields.String,
    'cost': fields.Integer,
    'observation': fields.String
})

dishes_model = api.model('dishes', {
    'dishes':fields.List(fields.Nested(dish_model))
})

@dishes_ns.route("/")
class Dishes(Resource):
    @dishes_ns.response(HTTPStatus.NOT_FOUND.value, 'There is no dish registered', message_model)
    @dishes_ns.response(HTTPStatus.OK.value, "Success", dishes_model)
    def get(self):
        """Return the list of all the dishes in database"""
        try:
            dishes = db.send_and_hear_back(f"SELECT * FROM menu_planner.dishes")
            dishes = {"dishes": [dict(zip(dish_model.keys(), dish)) for dish in dishes]}
            return dishes, HTTPStatus.OK
        except:
            return {}, HTTPStatus.NOT_FOUND
    
@dishes_ns.route("/<string:category>")
@dishes_ns.doc(params={"category":"Category of the dish"})
class DishesPerCategory(Resource):
    @dishes_ns.response(HTTPStatus.NOT_FOUND.value, 'There is no dish in this category', message_model)
    @dishes_ns.response(HTTPStatus.OK.value, 'Success', dishes_model)
    def get(self, category: str):
        try:
            dishes = db.send_and_hear_back(f"SELECT * FROM menu_planner.dishes WHERE category = '{category}'")
            dishes = {"dishes": [dict(zip(dish_model.keys(), dish)) for dish in dishes]}
            return dishes, HTTPStatus.OK
        except:
            return {}, HTTPStatus.NOT_FOUND