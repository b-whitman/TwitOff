from flask import Blueprint, jsonify, request, render_template, flash, current_app
from sklearn.linear_model import LogisticRegression
import numpy as np

from twitoff.models import User, Tweet, db
from twitoff.twitter_service import twitter_api_client
from twitoff.basilica_service import basilica_connection

my_routes = Blueprint("my_routes", __name__)
client = twitter_api_client()
basilica_client = basilica_connection()

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

@my_routes.route("/users/<string:screen_name>")
def show_user(screen_name=None):
    print("SHOWING USER:", screen_name)
    try:
        twitter_user = client.get_user(screen_name)
        print(type(twitter_user))
        db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
        print(db_user)

        db_user.screen_name = twitter_user.screen_name
        db_user.followers_count = twitter_user.followers_count
        db.session.add(db_user)
        db.session.commit()

        statuses = client.user_timeline(screen_name,
                                        tweet_mode="extended", 
                                        count=2, 
                                        exclude_replies=True, 
                                        include_rts=False)
        for status in statuses:
            print(status.full_text)

            db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
            print(db_tweet)

            db_tweet.user_id = status.author.id
            db_tweet.full_text = status.full_text
            embedding = basilica_client.embed_sentence(
                status.full_text,
                model="twitter")
            print("Embedding length:", len(embedding))
            db_tweet.embedding = embedding
            db.session.add(db_tweet)
            print("TWEET ADDED TO DB")
        print("COMMITTING TWEET TO DB...")
        db.session.commit()

        return render_template(
            "user_profile.html", 
            user=db_user,
            tweets=db_user.tweets
            )
    except Exception as e:
        print(e, "This is the exception")
        return jsonify({"message": "OOPS THERE WAS AN ERROR. PLEASE TRY ANOTHER USER"})

@my_routes.route("/predict", methods=["POST"])
def predict():
    """
    Determines which of two users are more likely to say a given tweet.
    Assumes users and their tweets have already been stored in the database.
    """

    print("PREDICTION REQUEST...")
    print("FORM DATA:", dict(request.form))
    sn1 = request.form["first_screen_name"]
    sn2 = request.form["second_screen_name"]
    tweet_text = request.form["tweet_text"]

    print("FETCHING TWEETS FROM THE DATABASE...")
    user1 = User.query.filter(User.screen_name == sn1).one()
    user2 = User.query.filter(User.screen_name == sn2).one()

    print("TRAINING THE MODEL...")

    user1_embeddings = np.array([tweet.embedding 
        for tweet 
        in user1.tweets])
    user2_embeddings = np.array([tweet.embedding
        for tweet
        in user2.tweets])
    embeddings = np.vstack([user1_embeddings, user2_embeddings])

    labels = np.concatenate([np.ones(len(user1.tweets)), 
        np.zeros(len(user2.tweets))]
        )
    print("LABELS", type(labels))

    classifier = LogisticRegression().fit(embeddings, labels)

    print("GETTING EMBEDDINGS FOR THE EXAMPLE TEXT...")
    tweet_embedding = basilica_client.embed_sentence(tweet_text, model="twitter")

    print("PREDICTING...")
    results = classifier.predict(np.array(tweet_embedding).reshape(1, -1))
    print(type(results), results.shape)
    print(results)
    
    return render_template("results.html",
        screen_name1=sn1,
        screen_name2=sn2,
        tweet_text=tweet_text,
        prediction_results=results
    )

# @my_routes.route("/users/create", methods=["POST"])
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

# @my_routes.route("/tweets/create", methods=["POST"])
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

# @my_routes.route("/get_tweets")
# def get_tweets():
#     tweets = []
#     client = current_app.config["TWITTER_API_CLIENT"]
#     statuses = client.user_timeline("elonmusk", tweet_mode='extended')
#     for status in statuses:
#         tweets.append({"id": status.id_str, "message": status.full_text})
#         db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
#         db.session.add(db_tweet)
#     print(tweets)
#     return jsonify(tweets)