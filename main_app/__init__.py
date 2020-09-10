from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
app.config['SECRET_KEY'] = "dkshkldjflsd"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///rcffutminna.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_db():
    db.create_all() 
    print("Database Created Successfully") 

from main_app import routes, user_routes
from main_app.models import User


@app.before_first_request
def create_db_command():
    create_db()
    find_user = User.query.filter_by(username="admin@rcffutminna1234").first()
    if not find_user:
        user = User(username="admin@rcffutminna1234",password="rcffutminna@admin1234")
        db.session.add(user)
        db.session.commit()
    else:
        print("User already exists!")
