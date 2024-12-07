from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Load database configuration
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "leave_db")
# Enable CORS for all routes
CORS(app)

# Load .env variables
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True



# Debugging: Print the database URI being used
print("Using database URI:", app.config["SQLALCHEMY_DATABASE_URI"])

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swagger_ui = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Leave API"}
)
app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)



# Register blueprints
from application.routes.auth_routes import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")
from application.routes.staff_routes import staff_bp
app.register_blueprint(staff_bp)



# Ensure database tables are created
# first_request = True

# @app.before_request
# def create_tables():
#     db.create_all()




@app.route("/")
def home():
    return {"message": "Welcome to Flask Leave API"}

if __name__ == "__main__":
    try:
       app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
    except Exception as e:
        print(f"Error: {e}")
