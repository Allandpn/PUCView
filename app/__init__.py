from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
import secrets



app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"



Session(app)
# bcrypt = Bcrypt(app)
# csrf = CSRFProtect(app)



from app import routes