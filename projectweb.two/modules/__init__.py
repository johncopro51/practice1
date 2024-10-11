from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = '4YrzfpQ4kGXjuP6w'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@host.docker.internal:5433/postgres'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)


app.permanent_session_lifetime = timedelta(days=30)
app.secret_key='Secret'


from modules import routes,guest_routes,chat_