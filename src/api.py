from flask_restx import Api, Resource, fields
from http import HTTPStatus

from .database import Database

api = Api(title='Natural Club Menu Planner', description='API for managing the menu planner web app, and talk to the SQL database')
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

@api.route("/dishes")
class Dishes(Resource):
    @api.response(HTTPStatus.NOT_FOUND, 'No collections exist', message_model)
    @api.response(HTTPStatus.OK, "Success", dishes_model)
    def get(self):
        """Return the list of all the dishes in database"""
        dishes = db.send_and_hear_back(f"SELECT * FROM menu_planner.dishes")
        return dishes