"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Event, Post
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

### USERS OPERATIONS ####

@app.route('/user', methods=['GET'])
def handle_get_users():
    all_users = User.query.all()
    response_body = {
        "data": [x.serialize() for x in all_users]
    }

    return jsonify(response_body), 200

### POSTS OPERATIONS ####

@app.route('/post', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'POST':
        keys_to_check = ["image_url", "description", "user_id"]
        new_post = request.get_json()
        # Check if all information was provided
        if all(key in new_post for key in keys_to_check):
            new_post = Post(image_url=new_post["image_url"], description=new_post["description"], user_id=new_post["user_id"])
            db.session.add(new_post)
            db.session.commit()
            return "New event added: " + new_post
    else:
        all_posts = Post.query.all()
        response_body = {
            "data": [x.serialize() for x in all_posts]
        }
        return jsonify(response_body), 200

### EVENTS OPERATIONS ####

@app.route('/event', methods=['GET', 'POST'])
def handle_events():
    if request.method == 'POST':
        keys_to_check = ["what", "where", "who"]
        new_event = request.get_json()
        # Check if all information was provided
        if all(key in new_event for key in keys_to_check):
            new_event = Event(what=new_event["what"], where=new_event["where"], who=new_event["who"])
            db.session.add(new_event)
            db.session.commit()
            return "New event added: " + new_event
    else:
        all_events = Event.query.all()
        response_body = {
            "data": [x.serialize() for x in all_events]
        }
        return jsonify(response_body), 200

@app.route('/event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = db.session.get(Event, event_id)
    db.session.delete(event)
    db.session.commit()

    return f"Event #{event_id} Deleted", 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
