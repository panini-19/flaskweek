from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

from app import routes