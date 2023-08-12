import logging
from flask import request
from flask_restx import Api, Resource
from http import HTTPStatus

from .database import Database
from . import models

logger = logging.getLogger('backend')

api = Api(title='Natural Club Menu Planner', description='API for managing the menu planner web app, and talk to the SQL database')
dishes_ns = api.namespace('dishes', description='Dish management')
db = Database()

@dishes_ns.route("/")
class Dishes(Resource):
    @dishes_ns.response(HTTPStatus.NOT_FOUND.value, 'There is no dish registered', models.message)
    @dishes_ns.response(HTTPStatus.OK.value, "Success", models.dishes)
    def get(self):
        """Return the list of all the dishes in database"""
        try:
            dishes = db.send_and_hear_back(f"SELECT * FROM menu_planner.dishes")
            dishes = {"dishes": [dict(zip(models.dish.keys(), dish)) for dish in dishes]}
            return dishes, HTTPStatus.OK
        except:
            return {}, HTTPStatus.NOT_FOUND

    @dishes_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR.value, 'It was not possible to register new dish', models.message)
    @dishes_ns.response(HTTPStatus.BAD_REQUEST.value, 'Dish already exists with the given name', models.message)
    @dishes_ns.response(HTTPStatus.OK.value, "Success", models.id)
    @dishes_ns.expect(models.dish, validate=True)
    def post(self):
        """Register new dish"""
        try:
            json_data = request.get_json()
            data = models.dish.to_sql(json_data)
            id = db.register('dishes', data)
            logger.info(f"New dish registered under id {id}")
            return id, HTTPStatus.OK
        except Exception as e:
            print(e)
        except:
            return models.message.to_sql({'message':'It was not possible to register new dish'}), HTTPStatus.INTERNAL_SERVER_ERROR

@dishes_ns.route("/<string:category>")
@dishes_ns.doc(params={"category":"Category of the dish"})
class DishesPerCategory(Resource):
    @dishes_ns.response(HTTPStatus.NOT_FOUND.value, 'There is no dish in this category', models.message)
    @dishes_ns.response(HTTPStatus.OK.value, 'Success', models.dishes)
    def get(self, category: str):
        """Get a list of dishes per category"""
        try:
            query = db.send_and_hear_back(f"SELECT * FROM menu_planner.dishes WHERE category = '{category}'")
            dishes = models.dish.from_sql(query)
            return dishes, HTTPStatus.OK
        except:
            return {}, HTTPStatus.NOT_FOUND


@dishes_ns.route("/<id>")
@dishes_ns.doc(params={"id":"id of the dish in the database"})
class DishId(Resource):
    @dishes_ns.response(HTTPStatus.NOT_FOUND.value, 'Id was not found', models.message)
    @dishes_ns.response(HTTPStatus.OK.value, 'Success', models.dish)
    def get(self, id:int):
        """Get the information of the dish of the given id"""
        try:
            query = db.send_and_hear_back(f"SELECT * FROM menu_planner.dishes WHERE id = {int(id)}")
            dishes = models.dish.from_sql(query)
            return dishes, HTTPStatus.OK
        except:
            return {}, HTTPStatus.NOT_FOUND
    
    @dishes_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR.value, 'Modification not possible', models.message)
    @dishes_ns.response(HTTPStatus.BAD_REQUEST.value, 'id not found', models.message)
    @dishes_ns.response(HTTPStatus.OK.value, 'Success', models.dish)
    @dishes_ns.expect(models.dish, validate=True)
    def put(self, id:int):
        """Modify the information of the dish of the given id"""
        try:
            json_data = request.get_json()
            data = models.dish.to_sql(json_data)
            successful, response = db.update('dishes', int(id), data)
            if successful:
                return {}, HTTPStatus.OK
            else:
                return {'message': str(response)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    @dishes_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR.value, 'Deletion not possible', models.message)
    @dishes_ns.response(HTTPStatus.BAD_REQUEST.value, 'id not found', models.message)
    @dishes_ns.response(HTTPStatus.OK.value, 'Success', models.dish)
    def delete(self, id:int):
        """Delete the information of the dish of the given id"""
        try:
            successful, response = db.delete('dishes', int(id))
            if successful:
                return {}, HTTPStatus.OK
            else:
                return {'message': str(response)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

def register_models(api:Api) -> None:
    """Register every declared model in models for documentation"""
    for model in vars(models).values():
        if isinstance(model, models.Model):
            logger.debug(f" Registered model {model.name}")
            api.models[model.name] = model

register_models(api)