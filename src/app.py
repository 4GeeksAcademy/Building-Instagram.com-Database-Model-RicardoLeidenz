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
from models import db, User, Post, Media
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
@app.route('/user', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        keys_to_check = ["username", "first_name", "last_name", "email"]
        new_user = request.get_json()
        # Check if all information was provided
        if all(key in new_user for key in keys_to_check):
            new_user = User(
                username=new_user["username"], first_name=new_user["first_name"], last_name=new_user["last_name"], email=new_user["email"])
            db.session.add(new_user)
            db.session.commit()
            return {"New User added": new_user.serialize()}, 200
    else:
        all_users = User.query.all()
        response_body = {
            "data": [x.serialize() for x in all_users]
        }
        return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
