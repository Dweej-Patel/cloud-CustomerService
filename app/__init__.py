from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from db_config import *

# Create the application server main class instance and call it 'application'
# Specific the path that identifies the static content and where it is.
application = Flask(__name__,
                    static_url_path='/static',
                static_folder='WebSite/static')

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


db = SQLAlchemy(application)
migrate = Migrate(application, db)

from app import views