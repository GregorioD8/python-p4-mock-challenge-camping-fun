#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Initialize Flask-RESTful for creating REST APIs
api = Api(app)

@app.route('/')
def home():
    return ''


# Define the Campers resource with GET and POST methods
class Campers(Resource):

    def get(self):
        # Handle GET request to retrieve all campers
        try:
            campers = Camper.query.all()
            
            #convert each camper object to dict
            new_campers = [c.to_dict(only=('id', 'name', 'age')) for c in campers]

            return new_campers, 200
        
        except:
            return {'error': 'Bad request'}, 400
        
    def post(self):
        #Handle POST request to create a new camper
        try:
            new_camper = Camper(
                name= request.json['name'],
                age = request.json['age']
            )
            db.session.add(new_camper)
            db.session.commit()

            return new_camper.to_dict(only=('id', 'name', 'age')), 201
        except:
            return { 'errors': ['validation errors']}, 400
        
# Add the Campers resource to the API at the /campers endpoint
api.add_resource(Campers, '/campers')

# Define the CampersById resource with GET method
class CampersById(Resource):

    def get(self, id):
        #Handle GET request to retrieve a camper by ID
        try:
            camper = Camper.query.filter(Camper.id == id).first().to_dict(only=('id', 'name', 'age', 'signups'))
            return camper, 200
        except:
            return {'error': 'Camper not found'}, 404
 
    def patch(self, id):
        # Handle PATCH request to update a comper by ID
        try:
            camper = Camper.query.filter_by(id=id).first()
            if not camper:
                return {'error': 'Camper not found'}, 404

            if 'name' in request.json:
                camper.name = request.json['name']
            if 'age' in request.json:
                camper.age = request.json['age']

            db.session.add(camper)
            db.session.commit()
            return camper.to_dict(only=('id', 'name', 'age')), 202
        except:
            return {'errors': ['validation errors']}, 400
        
# Add the CampersById resource to the API at the /campers endpoint
api.add_resource(CampersById, '/campers/<int:id>')

# Define the Activities resource with GET method
class Activities(Resource):
    def get(self):
        # Handle GET request to retrieve all activites
        try:
            activities = [activity.to_dict() for activity in Activity.query.all()]
            return activities, 200
        except:
            return {'error': 'Bad request'}, 400
        
# Add the Activities resource to the API at teh /activities endpoint
api.add_resource(Activities, '/activities')

# Define the ActivitiesById resource with PATCH and DELETE methods
class ActivitiesById(Resource):
    def patch(self, id):
        # Handle PATCH request to update an activity by ID
        try:
            activity = Activity.query.filter_by(id = id).first()
            if not activity:
                return {'error': 'Activity not found'}, 404
            
            if 'name' in request.json:
                activity.name = request.json['name']
            
            db.session.add(activity)
            db.session.commit()
            return activity.to_dict(), 202
        except:
            return {'error': '400: Validation error'}, 400
    
    def delete(self, id):
        # Handle DELETE request to delete an activity by ID
        try:
            activity = Activity.query.filter_by(id=id).first()
            if not activity:
                return {'error': 'Activity not found'}, 404
            db.session.delete(activity)
            db.session.commit()
            return {}, 204
        except:
            return {'error': 'Activity not found'}, 404
        
# Add the ActivitiesById resource to the API at the /activities/<int:id> endpoint
api.add_resource(ActivitiesById, '/activities/<int:id>')

# Difine the Signups resource with POST method
class Signups(Resource):

    def post(self):
        # Handle POST request to create a new signup
        try:
            signup = Signup(
                time= request.json['time'],
                camper_id= request.json['camper_id'],
                activity_id= request.json['activity_id']
            )
            db.session.add(signup)
            db.session.commit()

            return signup.to_dict(), 201
        except:
            return {'errors': ['validation errors']}, 400
        
# Add the Signups resource to the API at teh /signups endpoint
api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
