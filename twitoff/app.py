from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

from twitoff.models import db, User, Tweet, migrate
from twitoff.routes import my_routes
from twitoff.twitter_service import twitter_api_client

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", default="OOPS")

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["TWITTER_API_CLIENT"] = twitter_api_client()



    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(my_routes)

    return app




# #
# # ROUTING
# #

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/about")
# def about():
#     return "About Me"

# @app.route("/users")
# @app.route("/users.json")
# def users():
#     users = User.query.all()
#     print(type(users))
#     print(type(users[0]))

#     users_response = []
#     for u in users:
#         user_dict = u.__dict__
#         del user_dict["_sa_instance_state"]
#         users_response.append(user_dict)

#     return jsonify(users_response)

# @app.route("/users/create", methods=["POST"])
# def create_user():
#     print("CREATING A NEW USER...")
#     print("FORM DATA:", dict(request.form))
#     # return jsonify({"message": "CREATED OK (TODO)"})

#     if "name" in request.form:
#         name = request.form["name"]
#         print(name)
#         db.session.add(User(name=name))
#         db.session.commit()
#         return jsonify({"message": "CREATED OK", "name": name})
#     else:
#         return jsonify({"message": "OOPS"})

# @app.route("/tweets/create", methods=["POST"])
# def create_tweet():
#     print("CREATING A NEW TWEET...")
#     print("FORM DATA:", dict(request.form))

#     if "status" in request.form:
#         string = request.form["status"]
#         user_id = int(request.form["user_id"])
#         db.session.add(Tweet(status=string, user_id=user_id))
#         db.session.commit()
#         return jsonify({"message": "CREATED OK", "status": string})
#     else:
#         return jsonify({"message": "oops"})
