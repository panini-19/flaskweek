from flask import Blueprint

poke = Blueprint('poke', __name__, template_folder='poketemplates')
from . import routes
    