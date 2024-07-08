# from random import randint, choice as rc

# from faker import Faker

from app import app
from models import db, Activity, Signup, Camper
import os 

# fake = Faker()

def create_activities():
    activities = [
        Activity(name="Archery", difficulty=3),
        Activity(name="Swimming", difficulty=2),
        Activity(name="Hiking", difficulty=4),
        Activity(name="Canoeing", difficulty=3),
        Activity(name="Fishing", difficulty=1), 
    ]
    return activities

def create_campers():
    campers = [
        Camper(name="Alice Smith", age=12),
        Camper(name="Bob Johnson", age=10),
        Camper(name="Charlie Brown", age=14),
        Camper(name="David Wilson", age=9),
        Camper(name="Eva Green", age=15),
    ]
    return campers

def create_signups(activities, campers):
    signups = []
    signups.append(Signup(time=9, camper_id=campers[0].id, activity_id=activities[0].id))
    signups.append(Signup(time=11, camper_id=campers[1].id, activity_id=activities[1].id))
    signups.append(Signup(time=14, camper_id=campers[2].id, activity_id=activities[2].id))
    signups.append(Signup(time=19, camper_id=campers[3].id, activity_id=activities[3].id))
    signups.append(Signup(time=13, camper_id=campers[4].id, activity_id=activities[4].id))
    
    return signups

if __name__ == '__main__':

    if os.path.exists('app.db'):
        os.remove('app.db')

    with app.app_context():
        print('Creating a new database...')
        db.create_all()

        # print("Clearing db...")
        # Activity.query.delete()
        # Signup.query.delete()
        # Camper.query.delete()

        print("Seeding activities...")
        activities = create_activities()
        db.session.add_all(activities)
        db.session.commit()

        print("Seeding campers...")
        campers = create_campers()
        db.session.add_all(campers)
        db.session.commit()

        print("Seeding signups...")
        # Reload the activities and campers from the database to ensure ID's are correct
        activities = Activity.query.all()
        campers = Camper.query.all()
        signups = create_signups(activities, campers)
        db.session.add_all(signups)
        db.session.commit()

        print("Done seeding!")
