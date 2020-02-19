"""Entry point for TwitOff."""
from .app import create_app

# def create_app():
#     load_dotenv()

#     DATABASE_URL = os.getenv("DATABASE_URL", default="OOPS")

#     app = Flask(__name__)
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
#     app.config["TWITTER_API_CLIENT"] = twitter_api_client()

#     db.init_app(app)
#     migrate.init_app(app, db)

#     app.register_blueprint(my_routes)

#     return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
