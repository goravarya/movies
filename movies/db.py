from movies import app
from flask_sqlalchemy import SQLAlchemy
from config import Config


app.config.from_object(Config)

db = SQLAlchemy(app)
