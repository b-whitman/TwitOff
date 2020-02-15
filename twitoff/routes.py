from flask import Blueprint, jsonify, request, render_template#, current_app

from twitoff.models import User, Tweet, db

my_routes = Blueprint("my_routes", __name__)

@my_routes.route("/")
def index():
    return render_template("index.html")

@my_routes.route("/about")
def about():
    return "About Me"

@my_routes.route("/users")
@my_routes.route("/users.json")
def users():
    users = User.query.all()
    print(type(users))
    print(type(users[0]))

    users_response = []
    for u in users:
        user_dict = u.__dict__
        del user_dict["_sa_instance_state"]
        users_response.append(user_dict)

    return jsonify(users_response)

@my_routes.route("/users/create", methods=["POST"])
def create_user():
    print("CREATING A NEW USER...")
    print("FORM DATA:", dict(request.form))
    # return jsonify({"message": "CREATED OK (TODO)"})

    if "name" in request.form:
        name = request.form["name"]
        print(name)
        db.session.add(User(name=name))
        db.session.commit()
        return jsonify({"message": "CREATED OK", "name": name})
    else:
        return jsonify({"message": "OOPS"})

@my_routes.route("/tweets/create", methods=["POST"])
def create_tweet():
    print("CREATING A NEW TWEET...")
    print("FORM DATA:", dict(request.form))

    if "status" in request.form:
        string = request.form["status"]
        user_id = int(request.form["user_id"])
        db.session.add(Tweet(status=string, user_id=user_id))
        db.session.commit()
        return jsonify({"message": "CREATED OK", "status": string})
    else:
        return jsonify({"message": "oops"})
